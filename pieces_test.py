from board_and_pieces import Pawn
from board_and_pieces import Knight
from board_and_pieces import Bishop
from board_and_pieces import Rook
from board_and_pieces import Queen
from board_and_pieces import King
from board_and_pieces import Board
from board_and_pieces import Colour
import pytest

def read_board(board_file: str):
    f = open("./testing_boards/"+board_file)

    lines = f.read().split("\n")

    board_dict = {}
    for y in range(len(lines)):
        squares = lines[y].split()
        for x in range(len(squares)):
            if squares[x] == "K":
                board_dict[(x,y)] = King(x,y, Colour.WHITE)
            elif squares[x] == "k":
                board_dict[(x,y)] = King(x,y, Colour.BLACK)
            elif squares[x] == "Q":
                board_dict[(x,y)] = Queen(x,y, Colour.WHITE)
            elif squares[x] == "q":
                board_dict[(x,y)] = Queen(x,y, Colour.BLACK)
            elif squares[x] == "R":
                board_dict[(x,y)] = Rook(x,y, Colour.WHITE)
            elif squares[x] == "r":
                board_dict[(x,y)] = Rook(x,y, Colour.BLACK)
            elif squares[x] == "B":
                board_dict[(x,y)] = Bishop(x,y, Colour.WHITE)
            elif squares[x] == "b":
                board_dict[(x,y)] = Bishop(x,y, Colour.BLACK)
            elif squares[x] == "N":
                board_dict[(x,y)] = Knight(x,y, Colour.WHITE)
            elif squares[x] == "n":
                board_dict[(x,y)] = Knight(x,y, Colour.BLACK)
            elif squares[x] == "P":
                board_dict[(x,y)] = Pawn(x,y, Colour.WHITE)
            elif squares[x] == "p":
                board_dict[(x,y)] = Pawn(x,y, Colour.BLACK)
    return Board(board_dict)

def test_board():
    b = Board()
    print(b)
    knight_exists = False
    for piece in b.board_dict:
        if b.board_dict[piece].letter == "♞":
            knight_exists = True

    assert knight_exists

def test_knight():
    # use board1
    b = read_board("board1.txt")
    moves = b.board_dict[(1,7)].get_valid_moves(b, "", (0,0), (0,0))

    b4 = read_board("board4.txt")
    assert set(moves) == set([(2,5), (0,5)])

def test_bishop():
    # use board1
    b = read_board("board1.txt")
    moves = b.board_dict[(2,7)].get_valid_moves(b, "", (0,0), (0,0))
    assert set(moves) == set([])

    # use board 4
    b4 = read_board("board4.txt")
    moves4 = b4.board_dict[(6,3)].get_valid_moves(b4, "", (0,0), (0,0))

    
    assert set(moves4) == set([(5,2), (7,2), (7,4), (5,4), (4,5)])

def test_rook():
    #use board1
    b = read_board("board1.txt")
    moves = b.board_dict[(0,0)].get_valid_moves(b, "", (0,0), (0,0))
    assert set(moves) == set([])

    # using board4
    b4 = read_board("board4.txt")
    moves4 = b4.board_dict[(4,7)].get_valid_moves(b4, "", (0,0), (0,0))
    assert set(moves4) == set([(4,6), (4,5), (4,4), (4,3)])


def test_queen():
    #use board1
    b = read_board("board1.txt")
    moves = b.board_dict[(3,0)].get_valid_moves(b, "", (0,0), (0,0))
    assert set(moves) == set([])

    # using board4
    b4 = read_board("board4.txt")
    moves4 = b4.board_dict[(2,1)].get_valid_moves(b4, "", (0,0), (0,0))
    assert set(moves4) == set([(1,0), (3,0), (2,2), (3,2)])
