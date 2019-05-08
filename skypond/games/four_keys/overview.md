# Four Keys Game Overview
Four Keys is a simple gridworld game designed to be playable by machines. There are four keys randomly distributed throughout a n x n partially observable grid (typically 15 x 15). The first player to obtain all four keys wins.

The game is made more challenging by the inclusion of walls and other players racing to obtain the keys at the same time. After all keys on the board are obtained, it becomes a challenge to extract keys from other players by attacking.

## Movement
Players can only move one step at a time (subject to not being stunned) in any direction not containing a wall or another player.

## Attacking
Triggering an attack on an adjacent player _currently holding keys_ will cause that adjacent player to drop all keys in nearby spots and that player will be stunned for a number of moves.

## Players
Each player starts at a randomly selected base at the edge of the game board. At each turn the player can take the following actions:

## Action Space
- Nothing [0]
- Move one step Up [1] / Down [2] / Left [3] / Right [4]
- Drop key [6]
- Attack [7]

For example, return 2 (move down), to move down by one square. This action will be applied if the player's move recharge is at 100% and there's nothing blocking the target tile such as another player or a wall.

## State Space
The state space consists of a current observation frame, a set of previous observation frames, a breadcrumb frame, and a small supplement including additional stateful information about the player.

[Current Observation Frame (49)] [History Frames (49*4)] [Breadcrumb Frame (49)] [Supplement (5)]

### Common Observation Frame Items

- Open Space = 0
- Wall = 1
- Key = 2
- Player One = 3
- Other Player = 11

Additionally, some game variants feature a full state space including the specific player numbers. Those variants are:
- Player Two = 4
- Player Three = 5
- Player Four = 6
- Player Five = 7
- Player Six = 8
- Player Seven = 9
- Player Eight = 10

### Current Observation Frame

The observation window is a 7x7 subgrid (49 Squares) with the agent in the middle. As the agent moves around the board the observation window moves with the agent. Any tiles off the side of the board are represented as walls (Value 1). Each value corresponds to one of the observation frame items (defined above).

### Previous Observation Frames (History)
This provides the agent with limited memory into the last few frames, from the perspective of the agent itself.

Like the current observation frame, each history frame is a 7x7 observation window (49 Squares) that was provided at T-n timesteps equal to HISTORY_QUEUE_LENGTH (typically 4, see four_keys_constants.py for current configuration).

Note that the history is initialized with snapshots of the starting frame.

### Breadcrumb Frame
This provides information about how many times the agent has visited a given location, tracking up to 20 visits per tile (values remain constant at 20 after the 20th visit). Off-board areas - visible when near the side of a board - are indicated by value 21.

### Supplement
The tail end of the state space is set of five values providing additional context about the agent including the number of keys held, attack and movement recharges, and exact position on the board.

- Position Y
- Position X
- Number of Keys Held
- Attack Recharge Percent (0-100)
- Movement Recharge Percent (0-100)
