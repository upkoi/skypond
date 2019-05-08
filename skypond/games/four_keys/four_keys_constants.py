from __future__ import absolute_import

# The total number of keys in a normal game
# This might not change often :)
TOTAL_KEYS = 4

# How many turns to a full attack charge
# (Can't attack when below this number)
ATTACK_FULL_CHARGE = 20

# How many turns to a full movement movement recharge
# (Can't move when below this number)
MOVEMENT_FULL_CHARGE = 8

# How many items to keep in the memory queue
# (Position queue values are included in observation)
HISTORY_QUEUE_LENGTH = 4

# The index of the first player in the state enum
STARTING_PLAYER_NUMBER = 3

# The number of steps that a breadcrumb is active
BREADCRUMB_LIFESPAN = 1000
