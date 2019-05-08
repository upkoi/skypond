from __future__ import absolute_import

import numpy as np
import math
from ..base.shared_state import SharedState
from gym import error, spaces, utils
from gym.utils import seeding
from gym import wrappers
from .four_keys_board_items import FourKeysBoardItems
from .four_keys_actions import FourKeysActions
from .four_keys_constants import ATTACK_FULL_CHARGE,MOVEMENT_FULL_CHARGE,HISTORY_QUEUE_LENGTH,TOTAL_KEYS
from random import shuffle
import random
import operator

class FourKeysSharedState(SharedState):
    def __init__(self,side_length=15,num_seed_walls=6,wall_growth_factor=4,padding=1,seed=None):

        self._side_length = side_length
        self._num_seed_walls = num_seed_walls
        self._wall_growth_factor = wall_growth_factor
        self._padding = padding

        self._attached_envs = {}

        self.any_agent_won = False # Set to true when any agent obtains four keys

        # Controls if the observations are centered around the agent making the
        # observation
        self.agent_centered_observation = True

        # How many squares are visible to each agent (centered around agent)
        self.view_size = 7

        self.reward_shaping_mask_cache = {}

        self.seed(seed)

        # board is a snapshot of the current board with all layers
        # global_base_state is the board without keys or players
        # keys is a list of all of the keys on the board
        self.board,_,_,self.global_base_state,self.keys = self.build_board(side_length-(padding*2),num_seed_walls,wall_growth_factor,padding)

        size = side_length
        half_size = math.floor(size/2)
        self.starting_points = [(0,0),(size-1,size-1),(0,size-1),(size-1,0),(half_size,0),(half_size,size-1),(0,half_size),(size-1,half_size)]

        max_item=len(FourKeysBoardItems)

        # [Board] [History Items] [Breadcrumbs] [Supplement]
        # 2+HISTORY_QUEUE_LENGTH = size of [History Items] + ([Board] [Breadcrumbs])
        board_blank = [max_item]*(self.view_size**2 * (2+HISTORY_QUEUE_LENGTH))
        supplement = [side_length,side_length,4,100,100]
        high = np.array(board_blank+supplement)

        self.observation_space = spaces.Box(high*0, high, dtype=np.int8)

        self.action_space = spaces.Discrete(len(FourKeysActions))

    # Resets the board starting points used to place players
    def reset_starting_points(self):
        size = self._side_length
        half_size = math.floor(size/2)
        self.starting_points = [(0,0),(size-1,size-1),(0,size-1),(size-1,0),(half_size,0),(half_size,size-1),(0,half_size),(size-1,half_size)]

    # Shuffles the starting positions
    def shuffle_starting_points(self):
        shuffle(self.starting_points)

    # Generates an overview of game status
    def get_status(self):

        running = self.any_agent_won == False

        status = { 'running': running, 'players': [], 'keys': [] }

        for key in self.keys:
            status['keys'].append([int(key[0]),int(key[1])])

        for i in range(len(self._attached_envs)):
            env = self._attached_envs[i]
            status['players'].append(env.status)

        return status

    # Attaches a given environment. This is used during attack handling where one environment needs to change the internal state of another
    def register_attached_environment(self,env):
        self._attached_envs[env.number] = env

    # Generates an observation over the shared state, incorporating environment-specific values for convenience
    def generate_observation(self,position,history,keys,attack_recharge_percent,movement_recharge_percent,homogenize_player_numbers,breadcrumbs):
        supplement = [position[0], position[1], keys, attack_recharge_percent, movement_recharge_percent]

        return_board = self.get_observable_board(position,homogenize_player_numbers=homogenize_player_numbers)

        board_section = return_board

        visible_breadcrumbs = self.get_observable_breadcrumbs(position,breadcrumbs)

        # Append history if provided. Most recent items are at the end.
        for i in reversed(range(len(history))):
            board_section = np.concatenate((board_section, history[i]), axis=None)

        # [Current Observation] [Observation T-1] [Observation T-2] ... [ObservationT-n] [Breadcrumbs] [Supplement]
        return np.array(np.concatenate((board_section, visible_breadcrumbs, supplement), axis=None)), return_board, visible_breadcrumbs

    def get_observable_breadcrumbs(self,position,breadcrumbs,flat=True):
        if self.agent_centered_observation:
            # Translate breadcrumb map to have center tile be agent
            # Any unreachable areas are marked as unvisited

            # Maximum overflow to any side of the board is (size-1)/2
            # 7x7 board eventually becomes a 13x13

            margin = int((self.view_size - 1) / 2)
            full_side = self._side_length + margin*2

            margined_board = np.full((full_side,full_side),21)

            # Place breadcrumbs in center of larger placeholder
            margined_board[margin:margin+self._side_length,margin:margin+self._side_length] = breadcrumbs

            y = position[0]
            x = position[1]

            square_output = margined_board[y:y+self.view_size,x:x+self.view_size]

            if flat:
                return self.flatten(square_output)
            else:
                return square_output

        else:

            if flat:
                return self.breadcrumbs
            else:
                return self.squarify(self.breadcrumbs)

    def get_whole_square_board(self):
        return self.squarify(self.board)

    def get_observable_board(self,position,flat=True,homogenize_player_numbers=True):
        if self.agent_centered_observation:
            # Translate board to have center tile be agent
            # Any unreachable areas are marked as walls

            # Maximum overflow to any side of the board is (size-1)/2
            # 7x7 board eventually becomes a 13x13

            margin = int((self.view_size - 1) / 2)
            full_side = self._side_length + margin*2

            margined_board = np.full((full_side,full_side),FourKeysBoardItems.WALL)

            # If agent is at 6,6 unmargined they are at 3,3 margined

            board_square = self.squarify(np.copy(self.board))

            # If set, board at position is always first player
            # and all other player numbers are set to OTHER_PLAYER
            if homogenize_player_numbers:
                first_player = FourKeysBoardItems.PLAYER1
                last_player = FourKeysBoardItems.PLAYER8

                for y in range(self._side_length):
                    for x in range(self._side_length):
                        val = board_square[y,x]

                        if val >= first_player and val <= last_player:
                            board_square[y,x] = FourKeysBoardItems.OTHER_PLAYER

                board_square[position[0],position[1]] = first_player

            # Place board in center of larger placeholder
            margined_board[margin:margin+self._side_length,margin:margin+self._side_length] = board_square

            y = position[0]
            x = position[1]

            square_output = margined_board[y:y+self.view_size,x:x+self.view_size]

            if flat:
                return self.flatten(square_output)
            else:
                return square_output
        else:
            if flat:
                return self.board
            else:
                return self.squarify(self.board)

    # Adjusts or regenerates the current seed. Leave seed=None to use a random seed
    def seed(self, seed=None):
        self.rng, self._seed = seeding.np_random(seed)

    # Resets the core state using the established seed
    def reset(self):
        self.reward_shaping_mask_cache = {}
        self.board,_,_,self.global_base_state,self.keys = self.build_board(self._side_length-(self._padding*2),self._num_seed_walls,self._wall_growth_factor,self._padding)

    # Called when a key is picked by a player
    def key_consumed_handler(self, location, consuming_env):
        self.keys.remove(location)

        if consuming_env.keys == TOTAL_KEYS:
            self.any_agent_won = True

    # Called when a key is added to the board by an environment
    def new_key_handler(self, location, source_env):
        self.keys.append(location)

    # Handles state updates for adjacent players
    def attack_handler(self,adjacent_players_locs):
        for adjacent_player_loc in adjacent_players_locs:
            env_index = int(self.board[adjacent_player_loc] - 3)
            env = self._attached_envs[env_index]

            # Only hit the player if it has keys
            if env.keys > 0:
                env.receive_attack()

    # Turns a flat board into a sqaure board
    def squarify(self,board):
        side = int(math.sqrt(board.shape[0]))
        return board.reshape((side,side))

    # Turns a square board into a flat one
    def flatten(self,square_board):
        side = square_board.shape[0]
        return square_board.reshape((side*side))

    # Adds specified amount of padding to outside of board
    def pad(self,square_board,amount):
        side = square_board.shape[0]
        new_side = side+amount*2
        padded_board = np.zeros((new_side,new_side),dtype=np.int8)
        padded_board[amount:side+amount,amount:side+amount] = square_board
        return padded_board

    # Traverse all available spots on board reachable by current position,
    # marking mask where reachable
    def explore_to_mask(self,board,mask,pos):

        if mask[pos] == 1 or board[pos] == FourKeysBoardItems.WALL:
            return

        mask[pos] = 1

        max_item = board.shape[0]
        size = int(math.sqrt(board.shape[0]))

        # Left, right, down, up
        locs = [pos-1 if pos-1 >= 0 else None,
            pos+1 if pos+1 < max_item else None,
            pos+size if pos+size < max_item else None,
            pos-size if pos-size >= 0 else None,None]

        for loc in [loc for loc in locs if loc is not None]:
            self.explore_to_mask(board,mask,loc)

    # Creates a mask indicating which items are reachable
    def build_reachability_mask(self,board,padding):
        board_square = self.squarify(board)
        padded_board = self.pad(board_square,padding)

        padded_length = padded_board.shape[0]

        mask = np.zeros(padded_length**2,dtype=np.int8)

        # Any starting point on padded margin will work
        start = 0 # Top left

        flat_padded_board = self.flatten(padded_board)
        self.explore_to_mask(flat_padded_board,mask,start)

        return mask

    # Indicates how filled in an area surrounding a given position is
    def calculate_board_weight(self,board,pos,size,max_item):
        locs = [pos-1 if pos-1 >= 0 else None,
            pos+1 if pos+1 < max_item else None,
            pos+size if pos+size < max_item else None,
            pos-size if pos-size >= 0 else None,None]

        weight = 0

        for loc in locs:
            if loc is not None:
                weight += 1 if board[loc] != 0 else 0

        return weight

    # Indicates how filled in an area surrounding a given position is
    def calculate_board_weight(self,board,pos,size,max_item):
        locs = [pos-1 if pos-1 >= 0 else None,
            pos+1 if pos+1 < max_item else None,
            pos+size if pos+size < max_item else None,
            pos-size if pos-size >= 0 else None,None]

        weight = 0

        for loc in locs:
            if loc is not None:
                weight += 1 if board[loc] != 0 else 0

        return weight

    # Fills in any gaps and smooths over board construction
    def fill_gaps(self,board,reachability_mask):
        for i in range(len(board)):
            if reachability_mask[i] == 0 and board[i] == 0:
                board[i] = FourKeysBoardItems.WALL

    # Builds a distance based reward measure - intended to be normalized and adjusted by callers
    def build_current_distance_to_keys(self,square_board,position):

        closest_key_distance = -1
        closest_key_mask = None

        for key in self.keys:
            mask = self.build_path_mask(square_board,key,position)
            action,distance = self.get_shortest_path_action(square_board,mask,position)

            if distance < closest_key_distance or closest_key_distance == -1:
                closest_key_distance = distance
                closest_key_mask = mask

        if closest_key_distance != -1:

            return closest_key_distance

        else:
            return 999

    # Builds a list of allowable places for key placement and ideal probability
    # Probability is nudged in favor of high-weight areas (nooks)
    def build_key_possibilities(self,board,mask,key_placements,size,max_item):
        placements=[]
        probabilities=[]

        center_offset = math.floor(size/2)
        center = size*center_offset + center_offset

        for i in range(max_item):
            if mask[i] == 1 and not self.on_edge(i,size):
                # Reachable
                placements.append(i)

                probability = 200*(size*2 - self.distance(i,center,size))

                # Get probability (factor of how enclosed (board weight)
                # and distance from other keys) and center
                weight = self.calculate_board_weight(board,i,size,max_item)
                probability += 500 * weight

                for existing_key in key_placements:
                    probability += 100*self.distance(i,existing_key,size)

                probabilities.append(probability)

        prob_factor = 1 / sum(probabilities)
        probabilities = [prob_factor * p for p in probabilities]

        probability_mask = np.zeros(max_item)

        for p in range(len(placements)):
            probability_mask[placements[p]] = probabilities[p]

        return placements,probabilities,probability_mask

    # Gets allowed movements on a board given a current coordinate
    def get_allowable_movements(self,board,coordinate,only_consider_walls=False):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        actions = [FourKeysActions.UP,FourKeysActions.DOWN,FourKeysActions.LEFT,FourKeysActions.RIGHT]

        allowed_coordinates = []
        action_map = []

        max_offset = board.shape[0]-1
        candidate_index = 0

        for direction in directions:
            candidate = tuple(map(operator.add, coordinate, direction))

            if candidate[0] < 0 or candidate[0] > max_offset or candidate[1] < 0 or candidate[1] > max_offset:
                candidate_index += 1
                continue

            tile = board[candidate[0]][candidate[1]]

            allowed = False

            if only_consider_walls:
                allowed = not tile == FourKeysBoardItems.WALL
            else:
                allowed = tile == FourKeysBoardItems.EMPTY or tile == FourKeysBoardItems.KEY

            if allowed:
                allowed_coordinates.append(candidate)
                action_map.append(actions[candidate_index])

            candidate_index += 1

        return allowed_coordinates, action_map

    # Fills in a distance mask on a given board given a point
    def explore_path_cache_bfs(self,board,mask,point):

        queue = []
        queue.append(point)

        while queue:

            point = queue.pop(0)
            reachable_points,_ = self.get_allowable_movements(board,point,only_consider_walls=True)
            distance = mask[point[0],point[1]] + 1

            for new_point in reachable_points:

                mask_value = mask[new_point[0],new_point[1]]

                if mask_value == 999:
                    # Unexplored
                    mask[new_point[0],new_point[1]] = distance
                    queue.append(new_point)

        return mask

    # Builds a path planning mask indicating possible routes
    def build_path_mask(self,board,destination,current_location):

        cache_key = str(destination[0]) + '_' + str(destination[1])

        if cache_key in self.reward_shaping_mask_cache.keys():
            mask = self.reward_shaping_mask_cache[cache_key]
            return mask

        side_size = board.shape[0]
        mask = np.full((side_size,side_size),999)
        mask[destination[0],destination[1]] = 0
        mask = self.explore_path_cache_bfs(board,mask,destination)
        self.reward_shaping_mask_cache[cache_key] = mask
        return mask

    # Returns the coordinate with the smallest mask value
    def get_shortest_path_action(self,board,mask,coordinate):
        reachable_points,actions = self.get_allowable_movements(board,coordinate)

        shortest_path = 99999
        shortest_action = None

        for i in range(len(reachable_points)):
            point = reachable_points[i]
            mask_value = mask[point[0],point[1]]

            if mask_value < shortest_path:

                shortest_action = actions[i]
                shortest_path = mask_value

        return shortest_action,shortest_path

    # Returns distance between two coordinates on a flat board with side length size
    def distance(self,a,b,size):
        coordinates_a = np.array([math.floor(a / size),a%size])
        coordinates_b = np.array([math.floor(b / size),b%size])
        return np.linalg.norm(coordinates_a-coordinates_b)

    # Returns true if point is on the edge of the board
    def on_edge(self,position,size):

        # Horizontal edges (left and right)
        if position % size == size-1 or position % size == 0:
            return True

        # Vertical edges (top and bottom)
        if position <= size or position > size**2-size:
            return True

        return False

    # Constructs a board (including keys & walls) with a given specification
    def build_board(self,size=28,num_seed_walls=20,wall_growth_factor=8,padding=1):
        max_item = size**2
        padded_size = size+padding*2
        padded_max_item = padded_size**2

        board = np.zeros(max_item,dtype=np.int8)

        # Create seed walls
        walls = self.rng.choice(max_item-1,num_seed_walls)

        board[walls] = FourKeysBoardItems.WALL

        # Grow walls
        for i in range(wall_growth_factor):
            for pos in range(max_item):
                if board[pos] == FourKeysBoardItems.WALL:

                    locs = [pos-1 if pos-1 >= 0 else None,
                        pos+1 if pos+1 < max_item else None,
                        pos+size if pos+size < max_item else None,
                        pos-size if pos-size >= 0 else None,None]

                    next_item = self.rng.randint(0,4)
                    if locs[next_item] is not None:

                        next_item_pos = locs[next_item]
                        weight = self.calculate_board_weight(board,next_item_pos,size,max_item)

                        weight_ideal = weight < 3

                        # Skip over placing an item at a probability proportional
                        # to the weight of the board
                        if not weight_ideal:
                            skip_range = self.rng.randint(0,9-weight)
                            if skip_range != 0:
                                continue

                        board[next_item_pos] = FourKeysBoardItems.WALL

        # All sizes below this point should be padded
        reachability_mask = self.build_reachability_mask(board,padding)
        padded_board = self.flatten(self.pad(self.squarify(board),padding))

        # Apply any finishing touches to board
        self.fill_gaps(padded_board,reachability_mask)

        global_base_state = padded_board.copy()

        # Place keys
        unique_reachable_keys = 0
        keys = []
        key_coordinates = []
        key_probability_mask = []
        max_attempts = 1000
        attempts = 0

        # max_attempts stops corner cases with very small boards and large wall growth rate
        while unique_reachable_keys < TOTAL_KEYS and attempts < max_attempts:

            possibilities,key_probabilities,key_probability_mask = self.build_key_possibilities(padded_board,reachability_mask,keys,padded_size,padded_max_item)
            next_key = np.squeeze(self.rng.choice(possibilities,p=key_probabilities))

            if next_key not in keys:
                keys.append(next_key)
                key_coordinates.append((math.floor(next_key / padded_size),next_key%padded_size))
                unique_reachable_keys += 1

            attempts += 1

        padded_board[keys] = FourKeysBoardItems.KEY

        return padded_board, reachability_mask, key_probability_mask, global_base_state, key_coordinates
