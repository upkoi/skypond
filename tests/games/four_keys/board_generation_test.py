import math
import skypond
import numpy as np
from skypond.games.four_keys.four_keys_shared_state import FourKeysSharedState
from skypond.games.four_keys.four_keys_board_items import FourKeysBoardItems
from common import get_reachable_key_locations, count_keys, build_board, get_side_length

def ensure_walls_exist(board):
    return FourKeysBoardItems.WALL in board

def ensure_no_walls(board):
    return FourKeysBoardItems.WALL not in board

def edges_clear(board):
    side = get_side_length(board)
    square = board.reshape((side,side))

    for rotations in range(4):
        if np.sum(square[0]) != FourKeysBoardItems.EMPTY * side:
            return False
        np.rot90(square)

    return True

def test_create_blank_7x7_board():
    board = build_board(side_length=7,num_seed_walls=0)
    assert ensure_no_walls(board)
    assert get_side_length(board) == 7

def test_create_7x7_board():
    board = build_board(side_length=7,num_seed_walls=3)
    assert ensure_walls_exist(board)
    assert get_side_length(board) == 7

def test_blank_7x7_board_has_correct_key_count():
    board = build_board(side_length=7,num_seed_walls=0)
    assert get_side_length(board) == 7
    assert count_keys(board) == 4

def test_saturated_7x7_board_has_correct_key_count():
    board = build_board(side_length=7,num_seed_walls=3)
    assert get_side_length(board) == 7
    assert count_keys(board) == 4

def test_oversaturation_7x7_board_builds():
    # The wall structure prevents more than two keys from being added
    # This behavior will likely change in the future to try lower saturation automatically
    board = build_board(side_length=7,num_seed_walls=10)
    assert get_side_length(board) == 7
    assert ensure_walls_exist(board)
    assert count_keys(board) == 2

def test_saturated_7x7_board_has_correct_key_count():
    board = build_board(side_length=7,num_seed_walls=3)
    assert get_side_length(board) == 7
    assert count_keys(board) == 4

def test_saturated_7x7_board_has_clear_edges():
    # Edges should always be clear in the game design to allow movement on perimeter of board
    board = build_board(side_length=7,num_seed_walls=3)
    assert get_side_length(board) == 7
    assert count_keys(board) == 4
    assert edges_clear(board)

def test_saturated_7x7_board_all_keys_reachable():
    board = build_board(side_length=7,num_seed_walls=3)
    assert get_side_length(board) == 7
    assert count_keys(board) == 4
    assert len(get_reachable_key_locations(board)) == 4

def test_create_blank_15x15_board():
    board = build_board(side_length=15,num_seed_walls=0)
    assert ensure_no_walls(board)
    assert get_side_length(board) == 15

def test_create_15x15_board():
    board = build_board(side_length=15,num_seed_walls=3)
    assert ensure_walls_exist(board)
    assert get_side_length(board) == 15

def test_blank_15x15_board_has_correct_key_count():
    board = build_board(side_length=15,num_seed_walls=0)
    assert get_side_length(board) == 15
    assert count_keys(board) == 4

def test_saturated_15x15_board_has_correct_key_count():
    board = build_board(side_length=7,num_seed_walls=5)
    assert get_side_length(board) == 15
    assert count_keys(board) == 4

def test_saturated_15x15_board_has_correct_key_count():
    board = build_board(side_length=15,num_seed_walls=5)
    assert get_side_length(board) == 15
    assert count_keys(board) == 4

def test_saturated_15x15_board_has_clear_edges():
    # Edges should always be clear in the game design to allow movement on perimeter of board
    board = build_board(side_length=15,num_seed_walls=5)
    assert get_side_length(board) == 15
    assert count_keys(board) == 4
    assert edges_clear(board)

def test_saturated_15x15_board_all_keys_reachable():
    board = build_board(side_length=15,num_seed_walls=5)
    assert get_side_length(board) == 15
    assert count_keys(board) == 4
    assert len(get_reachable_key_locations(board)) == 4


def test_create_blank_30x30_board():
    board = build_board(side_length=30,num_seed_walls=0)
    assert ensure_no_walls(board)
    assert get_side_length(board) == 30

def test_create_30x30_board():
    board = build_board(side_length=30,num_seed_walls=3)
    assert ensure_walls_exist(board)
    assert get_side_length(board) == 30

def test_blank_30x30_board_has_correct_key_count():
    board = build_board(side_length=30,num_seed_walls=0)
    assert get_side_length(board) == 30
    assert count_keys(board) == 4

def test_saturated_30x30_board_has_correct_key_count():
    board = build_board(side_length=7,num_seed_walls=5)
    assert get_side_length(board) == 30
    assert count_keys(board) == 4

def test_saturated_30x30_board_has_correct_key_count():
    board = build_board(side_length=30,num_seed_walls=5)
    assert get_side_length(board) == 30
    assert count_keys(board) == 4

def test_saturated_30x30_board_has_clear_edges():
    board = build_board(side_length=30,num_seed_walls=5)
    assert get_side_length(board) == 30
    assert count_keys(board) == 4
    assert edges_clear(board)

def test_saturated_30x30_board_all_keys_reachable():
    board = build_board(side_length=30,num_seed_walls=5)
    assert get_side_length(board) == 30
    assert count_keys(board) == 4
    assert len(get_reachable_key_locations(board)) == 4
