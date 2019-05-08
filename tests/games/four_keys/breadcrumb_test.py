import math
import skypond
import numpy as np
from skypond.games.four_keys.four_keys_environment import FourKeysEnvironment
from skypond.games.four_keys.four_keys_shared_state import FourKeysSharedState
from skypond.games.four_keys.four_keys_board_items import FourKeysBoardItems
from skypond.games.four_keys.four_keys_actions import FourKeysActions
from skypond.games.four_keys.four_keys_constants import ATTACK_FULL_CHARGE, MOVEMENT_FULL_CHARGE, BREADCRUMB_LIFESPAN
from common import setup, assert_position, count_keys, count_all_breadcrumbs, get_breadcrumb_value

# (Breadcrumbs are the position tracks that are tracked by the environment)

def test_breadcrumbs_initialize_empty():
    envs,shared_state = setup()
    env = envs[0]
    assert count_all_breadcrumbs(env) == 0

def test_breadcrumbs_increase_with_movement():
    envs,shared_state = setup()
    env = envs[0]
    env.step(FourKeysActions.DOWN)
    assert count_all_breadcrumbs(env) == 1

def test_breadcrumbs_placed_correctly():
    envs,shared_state = setup()
    env = envs[0]
    env.step(FourKeysActions.DOWN)
    assert get_breadcrumb_value(env,(0,0)) == 1
    assert get_breadcrumb_value(env,(1,0)) == 0

def test_breadcrumbs_increment_in_place():
    envs,shared_state = setup()
    env = envs[0]
    env.step(FourKeysActions.DOWN)
    env.step(FourKeysActions.UP)
    env.step(FourKeysActions.DOWN)
    assert get_breadcrumb_value(env,(0,0)) == 2
    assert get_breadcrumb_value(env,(1,0)) == 1

def test_breadcrumbs_cap_at_limit():
    envs,shared_state = setup()
    env = envs[0]

    for i in range(50):
        env.step(FourKeysActions.DOWN)
        env.step(FourKeysActions.UP)

    assert get_breadcrumb_value(env,(0,0)) == 20
    assert get_breadcrumb_value(env,(1,0)) == 20

def test_breadcrumbs_cap_at_limit():
    envs,shared_state = setup(side_length=15)
    env = envs[0]

    for i in range(15):
        for i in range(3):
            for i in range(15):
                env.step(FourKeysActions.DOWN)
            for i in range(15):
                env.step(FourKeysActions.UP)

        env.step(FourKeysActions.RIGHT)

    for i in range(10):
        env.step(FourKeysActions.NOTHING)

    assert count_all_breadcrumbs(env) == BREADCRUMB_LIFESPAN

    assert get_breadcrumb_value(env,(0,0)) == 0
    assert get_breadcrumb_value(env,(0,5)) == 7
    #print(env.breadcrumbs) # for more explanation
