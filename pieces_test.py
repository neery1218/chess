from board_and_pieces import Board
import pytest

def test_board():
    b = Board()
    
    knight_exists = False
    for piece in b.board_dict:
        if b.board_dict[piece].letter == "K":
            knight_exists = True
    
    assert knight_exists
