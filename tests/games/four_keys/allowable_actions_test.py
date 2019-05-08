import math
import skypond
import numpy as np
from skypond.games.four_keys.four_keys_environment import FourKeysEnvironment
from skypond.games.four_keys.four_keys_shared_state import FourKeysSharedState
from skypond.games.four_keys.four_keys_board_items import FourKeysBoardItems
from skypond.games.four_keys.four_keys_actions import FourKeysActions
from common import setup, assert_position, count_keys

def test_top_left_empty_move_down_ok():
    envs,shared_state = setup()
    env = envs[0]
    assert_position(env,shared_state,(0,0))
    env.step(FourKeysActions.DOWN)
    assert_position(env,shared_state,(1,0))

def test_top_left_empty_move_left_not_ok():
    envs,shared_state = setup()
    env = envs[0]
    assert_position(env,shared_state,(0,0))
    env.step(FourKeysActions.LEFT)
    assert_position(env,shared_state,(0,0))

def test_top_left_empty_move_up_not_ok():
    envs,shared_state = setup()
    env = envs[0]
    assert_position(env,shared_state,(0,0))
    env.step(FourKeysActions.UP)
    assert_position(env,shared_state,(0,0))

def test_top_left_empty_move_right_ok():
    envs,shared_state = setup()
    env = envs[0]
    assert_position(env,shared_state,(0,0))
    env.step(FourKeysActions.RIGHT)
    assert_position(env,shared_state,(0,1))

def test_inside_board_move_down_ok():
    envs,shared_state = setup(positions=[(1,1)])
    env = envs[0]
    assert_position(env,shared_state,(1,1))
    env.step(FourKeysActions.DOWN)
    assert_position(env,shared_state,(2,1))

def test_inside_board_move_right_ok():
    envs,shared_state = setup(positions=[(1,1)])
    env = envs[0]
    assert_position(env,shared_state,(1,1))
    env.step(FourKeysActions.RIGHT)
    assert_position(env,shared_state,(1,2))

def test_inside_board_move_up_ok():
    envs,shared_state = setup(positions=[(1,1)])
    env = envs[0]
    assert_position(env,shared_state,(1,1))
    env.step(FourKeysActions.UP)
    assert_position(env,shared_state,(0,1))

def test_inside_board_move_left_ok():
    envs,shared_state = setup(positions=[(1,1)])
    env = envs[0]
    assert_position(env,shared_state,(1,1))
    env.step(FourKeysActions.LEFT)
    assert_position(env,shared_state,(1,0))

def test_inside_board_wall_block():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,2)])
    env = envs[0]
    assert_position(env,shared_state,(1,1))
    env.step(FourKeysActions.RIGHT)
    assert_position(env,shared_state,(1,1))

def test_inside_board_wall_multi_step_block():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,3)])
    env = envs[0]
    assert_position(env,shared_state,(1,1))
    env.step(FourKeysActions.RIGHT)
    env.step(FourKeysActions.RIGHT)
    assert_position(env,shared_state,(1,2))

def test_inside_board_wall_not_block():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,3)])
    env = envs[0]
    assert_position(env,shared_state,(1,1))
    env.step(FourKeysActions.RIGHT)
    assert_position(env,shared_state,(1,2))

def test_inside_board_wall_not_block():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,3)])
    env = envs[0]
    assert_position(env,shared_state,(1,1))
    env.step(FourKeysActions.RIGHT)
    assert_position(env,shared_state,(1,2))

def test_key_not_block():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    assert_position(env,shared_state,(1,1))
    env.step(FourKeysActions.RIGHT)
    assert_position(env,shared_state,(1,2))

def test_key_pickup():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    assert env.keys == 0
    env.step(FourKeysActions.RIGHT)
    assert env.keys == 1

def test_key_remove_from_game():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    assert len(shared_state.keys) == 5
    assert count_keys(shared_state.board) == 5
    env.step(FourKeysActions.RIGHT)
    assert len(shared_state.keys) == 4
    assert count_keys(shared_state.board) == 4

def test_drop_key_add_to_board():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    env.step(FourKeysActions.RIGHT) # Pickup key
    assert count_keys(shared_state.board) == 4
    env.step(FourKeysActions.DROP_KEY)
    assert count_keys(shared_state.board) == 5

def test_drop_key_remove_from_inventory():
    envs,shared_state = setup(positions=[(1,1)],walls=[(1,3)],additional_keys=[(1,2)])
    env = envs[0]
    env.step(FourKeysActions.RIGHT) # Pickup key
    assert env.keys == 1
    env.step(FourKeysActions.DROP_KEY)
    assert env.keys == 0
