import math
import skypond
import numpy as np
from skypond.games.four_keys.four_keys_environment import FourKeysEnvironment
from skypond.games.four_keys.four_keys_shared_state import FourKeysSharedState
from skypond.games.four_keys.four_keys_board_items import FourKeysBoardItems
from skypond.games.four_keys.four_keys_actions import FourKeysActions

def explore(board,explored_locations,found_key_locations,pos):

    if explored_locations[pos] == 1 or board[pos] == FourKeysBoardItems.WALL:
        return

    explored_locations[pos] = 1

    if board[pos] == FourKeysBoardItems.KEY:
        found_key_locations.append(pos)

    max_item = board.shape[0]
    size = int(math.sqrt(board.shape[0]))

    # Left, right, down, up
    locs = [pos-1 if pos-1 >= 0 else None,
        pos+1 if pos+1 < max_item else None,
        pos+size if pos+size < max_item else None,
        pos-size if pos-size >= 0 else None,None]

    for loc in [loc for loc in locs if loc is not None]:
        explore(board,explored_locations,found_key_locations,loc)

def get_reachable_key_locations(board,start=0):
    explored_locations = np.zeros(len(board),dtype=np.int8)
    found_key_locations = []

    explore(board,explored_locations,found_key_locations,start)

    return found_key_locations

# Note: position is (y,x)
def setup(side_length=7,positions=[(0,0)],walls=[],additional_keys=[]):
    shared_state = FourKeysSharedState(side_length,0,0,seed=42)

    player_index = 0
    for pos in positions:
        shared_state.starting_points[player_index] = pos
        player_index += 1

    envs = []

    for i in range(len(positions)):
        env = FourKeysEnvironment(shared_state,i)
        envs.append(env)

    for wall in walls:
        pos = wall[0]*side_length + wall[1]
        shared_state.board[pos] = FourKeysBoardItems.WALL

    for key in additional_keys:
        # Might be a good idea to refactor this into an add_key() method - although not a common use case
        shared_state.keys.append(key)
        pos = key[0]*side_length + key[1]
        shared_state.board[pos] = FourKeysBoardItems.KEY

    return envs,shared_state

def count_keys(board):
    return np.count_nonzero(board == FourKeysBoardItems.KEY)

def assert_position(env,shared_state,position,player=FourKeysBoardItems.PLAYER1):

    side = int(math.sqrt(shared_state.board.shape[0]))
    square = shared_state.board.reshape((side,side))

    assert env.position == position
    assert square[position[0]][position[1]] == player

def build_board(side_length=15,num_seed_walls=6,wall_growth_factor=4):
    shared_state = FourKeysSharedState(side_length,num_seed_walls,wall_growth_factor,seed=42)
    return shared_state.board

def count_keys(board):
    return np.count_nonzero(board == FourKeysBoardItems.KEY)

def get_side_length(board):
    return int(math.sqrt(board.shape[0]))

def count_all_breadcrumbs(env):
    return np.sum(env.breadcrumbs)

def get_breadcrumb_value(env,pos):
    bc = env.breadcrumbs
    return bc[pos[0]][pos[1]]
