import math
import skypond
import numpy as np
from skypond.games.four_keys.four_keys_environment import FourKeysEnvironment
from skypond.games.four_keys.four_keys_shared_state import FourKeysSharedState
from skypond.games.four_keys.four_keys_board_items import FourKeysBoardItems
from skypond.games.four_keys.four_keys_actions import FourKeysActions
from skypond.games.four_keys.four_keys_constants import ATTACK_FULL_CHARGE, MOVEMENT_FULL_CHARGE
from common import setup, assert_position, count_keys

def test_attack_start_at_zero_recharge():
    envs,shared_state = setup(positions=[(1,0)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    assert env.attack_recharge == 0

def test_attack_recharge_with_steps():
    envs,shared_state = setup(positions=[(1,0)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    env.step(FourKeysActions.NOTHING)
    assert env.attack_recharge == 1

def test_attack_recharge_no_change_on_movement_when_full():
    envs,shared_state = setup(positions=[(1,0)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]

    # Recharge
    for i in range(20):
        env.step(FourKeysActions.NOTHING)

    assert env.attack_recharge == ATTACK_FULL_CHARGE
    env.step(FourKeysActions.RIGHT)
    assert env.attack_recharge == ATTACK_FULL_CHARGE

def test_attack_recharge_no_change_on_key_pickup():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]

    # Recharge
    for i in range(20):
        env.step(FourKeysActions.NOTHING)

    assert env.attack_recharge == ATTACK_FULL_CHARGE
    env.step(FourKeysActions.RIGHT)
    assert env.attack_recharge == ATTACK_FULL_CHARGE

def test_attack_recharge_no_change_with_no_adjacent_players():
    envs,shared_state = setup(positions=[(1,0)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]

    # Recharge
    for i in range(20):
        env.step(FourKeysActions.NOTHING)

    assert env.attack_recharge == ATTACK_FULL_CHARGE
    env.step(FourKeysActions.ATTACK)
    assert env.attack_recharge == ATTACK_FULL_CHARGE

def test_attack_recharge_decrease_with_adjacent_players():
    envs,shared_state = setup(positions=[(1,0),(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]

    # Recharge
    for i in range(20):
        env.step(FourKeysActions.NOTHING)

    assert env.attack_recharge == ATTACK_FULL_CHARGE
    env.step(FourKeysActions.ATTACK)
    assert env.attack_recharge == 1


def test_attack_no_effect_below_recharge():
    envs,shared_state = setup(positions=[(1,0),(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    env2 = envs[1]

    # Partial recharge
    for i in range(10):
        env.step(FourKeysActions.NOTHING)
        env2.step(FourKeysActions.NOTHING)

    env2.step(FourKeysActions.RIGHT) # Pickup key
    env2.step(FourKeysActions.LEFT)

    assert env2.keys == 1

    assert env.attack_recharge < ATTACK_FULL_CHARGE
    env.step(FourKeysActions.ATTACK)
    assert env.attack_recharge > 1
    assert env2.keys == 1

def test_attack_hit_player_when_charged_adjacent():
    envs,shared_state = setup(positions=[(1,0),(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    env2 = envs[1]

    # Fully recharge
    for i in range(20):
        env.step(FourKeysActions.NOTHING)
        env2.step(FourKeysActions.NOTHING)

    env2.step(FourKeysActions.RIGHT) # Pickup key
    env2.step(FourKeysActions.LEFT)

    assert env2.keys == 1
    assert count_keys(shared_state.board) == 4

    assert env.attack_recharge == ATTACK_FULL_CHARGE

    env.step(FourKeysActions.ATTACK)
    assert env.attack_recharge == 1
    assert env2.keys == 0
    assert count_keys(shared_state.board) == 5

def test_attack_miss_player_when_charged_not_adjacent():
    envs,shared_state = setup(positions=[(1,0),(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    env2 = envs[1]

    # Fully recharge
    for i in range(20):
        env.step(FourKeysActions.NOTHING)
        env2.step(FourKeysActions.NOTHING)

    env2.step(FourKeysActions.RIGHT) # Pickup key
    env2.step(FourKeysActions.LEFT)
    env2.step(FourKeysActions.RIGHT)

    assert env2.keys == 1
    assert count_keys(shared_state.board) == 4

    assert env.attack_recharge == ATTACK_FULL_CHARGE

    env.step(FourKeysActions.ATTACK)
    assert env.attack_recharge == ATTACK_FULL_CHARGE
    assert env2.keys == 1
    assert count_keys(shared_state.board) == 4

def test_attack_player_movement_recharge_impacted():
    envs,shared_state = setup(positions=[(1,0),(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    env2 = envs[1]

    # Fully recharge
    for i in range(20):
        env.step(FourKeysActions.NOTHING)
        env2.step(FourKeysActions.NOTHING)

    env2.step(FourKeysActions.RIGHT) # Pickup key
    env2.step(FourKeysActions.LEFT)

    assert env2.keys == 1
    assert count_keys(shared_state.board) == 4

    assert env.attack_recharge == ATTACK_FULL_CHARGE

    env.step(FourKeysActions.ATTACK)
    assert env.attack_recharge == 1
    assert env2.move_recharge == 0
    assert count_keys(shared_state.board) == 5

# A subtlety of the game. Attacking a player with no keys has no impact on them.
def test_attack_player_movement_recharge_not_impacted_without_keys():
    envs,shared_state = setup(positions=[(1,0),(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    env2 = envs[1]

    # Fully recharge
    for i in range(20):
        env.step(FourKeysActions.NOTHING)
        env2.step(FourKeysActions.NOTHING)

    assert env2.keys == 0
    assert env.attack_recharge == ATTACK_FULL_CHARGE
    env.step(FourKeysActions.ATTACK)

    assert env.attack_recharge == 1
    assert env2.move_recharge == MOVEMENT_FULL_CHARGE
    assert env2.attack_recharge == ATTACK_FULL_CHARGE

def test_attack_receiving_player_with_keys_unable_to_move():
    envs,shared_state = setup(positions=[(1,0),(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    env2 = envs[1]

    # Fully recharge
    for i in range(20):
        env.step(FourKeysActions.NOTHING)
        env2.step(FourKeysActions.NOTHING)

    env2.step(FourKeysActions.RIGHT) # Pickup key
    env2.step(FourKeysActions.LEFT)

    env.step(FourKeysActions.ATTACK)

    assert env.attack_recharge == 1
    assert env2.move_recharge == 0
    assert_position(env2,shared_state,(1,1),player=FourKeysBoardItems.PLAYER2)
    env2.step(FourKeysActions.RIGHT)
    assert_position(env2,shared_state,(1,1),player=FourKeysBoardItems.PLAYER2)
