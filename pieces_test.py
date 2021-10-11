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
                board_dict[(x, y)] = King(x, y, Colour.WHITE)
            elif squares[x] == "k":
                board_dict[(x, y)] = King(x, y, Colour.BLACK)
            elif squares[x] == "Q":
                board_dict[(x, y)] = Queen(x, y, Colour.WHITE)
            elif squares[x] == "q":
                board_dict[(x, y)] = Queen(x, y, Colour.BLACK)
            elif squares[x] == "R":
                board_dict[(x, y)] = Rook(x, y, Colour.WHITE)
            elif squares[x] == "r":
                board_dict[(x, y)] = Rook(x, y, Colour.BLACK)
            elif squares[x] == "B":
                board_dict[(x, y)] = Bishop(x, y, Colour.WHITE)
            elif squares[x] == "b":
                board_dict[(x, y)] = Bishop(x, y, Colour.BLACK)
            elif squares[x] == "N":
                board_dict[(x, y)] = Knight(x, y, Colour.WHITE)
            elif squares[x] == "n":
                board_dict[(x, y)] = Knight(x, y, Colour.BLACK)
            elif squares[x] == "P":
                board_dict[(x, y)] = Pawn(x, y, Colour.WHITE)
            elif squares[x] == "p":
                board_dict[(x, y)] = Pawn(x, y, Colour.BLACK)
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
    moves = b.board_dict[(1, 7)].get_valid_moves(b, "", (0, 0), (0, 0))

    b4 = read_board("board4.txt")
    assert set(moves) == set([(2, 5), (0, 5)])


def test_bishop():
    # use board1
    b = read_board("board1.txt")
    moves = b.board_dict[(2, 7)].get_valid_moves(b, "", (0, 0), (0, 0))
    assert set(moves) == set([])

    # use board 4
    b4 = read_board("board4.txt")
    moves4 = b4.board_dict[(6, 3)].get_valid_moves(b4, "", (0, 0), (0, 0))

    assert set(moves4) == set([(5, 2), (7, 2), (7, 4), (5, 4), (4, 5)])


def test_rook():
    # use board1
    b = read_board("board1.txt")
    moves = b.board_dict[(0, 0)].get_valid_moves(b, "", (0, 0), (0, 0))
    assert set(moves) == set([])

    # using board4
    b4 = read_board("board4.txt")
    moves4 = b4.board_dict[(4, 7)].get_valid_moves(b4, "", (0, 0), (0, 0))
    assert set(moves4) == set([(4, 6), (4, 5), (4, 4), (4, 3)])


def test_queen():
    # use board1
    b = read_board("board1.txt")
    moves = b.board_dict[(3, 0)].get_valid_moves(b, "", (0, 0), (0, 0))
    assert set(moves) == set([])

    # using board4
    b4 = read_board("board4.txt")
    moves4 = b4.board_dict[(2, 1)].get_valid_moves(b4, "", (0, 0), (0, 0))
    assert set(moves4) == set([(1, 0), (3, 0), (2, 2), (3, 2)])


def test_pawn():
    # use board1
    b = read_board("board1.txt")
    moves = b.board_dict[(0, 6)].get_valid_moves(b, "", (0, 0), (0, 0))
    assert set(moves) == set([(0, 5), (0, 4)])
    # test pawn capture (non en-passant)
    b5 = read_board("board5.txt")
    b5.board_dict[(3, 3)].has_moved = True
    b5.board_dict[(4, 4)].has_moved = True
    moves5 = b5.board_dict[(3, 3)].get_valid_moves(b5, "", (0, 0), (0, 0))
    assert set(moves5) == set([(4, 4), (3, 4)])
    # test pawn capture (en-passant)
    b6 = read_board("board6.txt")
    last_moved = "♙"
    initial_pos = (1, 1)
    final_pos = (1, 3)
    b6.board_dict[(0, 3)].has_moved = True
    moves6 = b6.board_dict[(0, 3)].get_valid_moves(
        b6, last_moved, initial_pos, final_pos)
    assert set(moves6) == set([(0, 2), (1, 2, -1)])


def test_piece_copy():
    p = Pawn(1, 1, Colour.WHITE)
    d = p.deepcopy()

    assert p.x == d.x
    assert p.y == d.y
    assert p.colour == d.colour
    assert p.has_moved == d.has_moved
    assert p.letter == d.letter
    assert not p is d


def test_board_copy():
    board = Board()

    copy_board = board.deepcopy()

    assert not copy_board is board

    for piece in board.board_dict:
        assert piece in copy_board.board_dict
        assert board.board_dict[piece].x == copy_board.board_dict[piece].x
        assert board.board_dict[piece].y == copy_board.board_dict[piece].y
        assert board.board_dict[piece].colour == copy_board.board_dict[piece].colour
        assert board.board_dict[piece].has_moved == copy_board.board_dict[piece].has_moved
        assert board.board_dict[piece].letter == copy_board.board_dict[piece].letter


def test_check():
    board = read_board("board_check.txt")

    assert board.in_check(Colour.WHITE) == False
    assert board.in_check(Colour.BLACK) == True


def test_move_without_castling():
    board = read_board("board3.txt")
    # want to move the white bishop from (5,7) to (1,3)
    board.make_move((5, 7), (1, 3))
    # test normal move
    move_board = read_board("board_3_bishop_move.txt")
    move_board.board_dict[(1, 3)].has_moved = True
    for piece in board.board_dict:
        assert piece in move_board.board_dict
        assert board.board_dict[piece].x == move_board.board_dict[piece].x
        assert board.board_dict[piece].y == move_board.board_dict[piece].y
        assert board.board_dict[piece].colour == move_board.board_dict[piece].colour
        assert board.board_dict[piece].has_moved == move_board.board_dict[piece].has_moved
        assert board.board_dict[piece].letter == move_board.board_dict[piece].letter
    # test en passant (moving the white pawn from (0,3) to (1,2)) and deleting the pawn at (1,3)
    board2 = read_board("board6.txt")
    en_passant_board = read_board("board_6_enpassant_moved.txt")
    board2.make_move((0, 3), (1, 2, -1))
    en_passant_board.board_dict[(1, 2)].has_moved = True
    for piece in board2.board_dict:
        assert piece in en_passant_board.board_dict
        assert board2.board_dict[piece].x == en_passant_board.board_dict[piece].x
        assert board2.board_dict[piece].y == en_passant_board.board_dict[piece].y
        assert board2.board_dict[piece].colour == en_passant_board.board_dict[piece].colour
        assert board2.board_dict[piece].has_moved == en_passant_board.board_dict[piece].has_moved
        assert board2.board_dict[piece].letter == en_passant_board.board_dict[piece].letter


def test_can_castle():
    # default starting board, shouldn't be able to castle either way
    board = read_board("board1.txt")
    assert board.board_dict[(4, 0)].can_castle(board) == (False, False)
    # kingside should be true in this case
    board2 = read_board("board_kingside_true.txt")
    assert board2.board_dict[(4, 7)].can_castle(board2) == (False, True)
    # kingside should be false in this case
    board3 = read_board("board_kingside_false.txt")
    assert board3.board_dict[(4, 7)].can_castle(board3) == (False, False)
    # test the blocking of the castle
    board4 = read_board("board_white_castle_block.txt")
    assert board4.board_dict[(4, 7)].can_castle(board4) == (True, False)
    assert board4.board_dict[(4, 0)].can_castle(board4) == (True, True)


def test_castle_move():
    board = read_board("board_white_castle_block.txt")
    board.make_move((4, 0), ("Queenside",))
    castled_board = read_board("board_black_queenside_move.txt")
    castled_board.board_dict[(2, 0)].has_moved = True
    castled_board.board_dict[(3, 0)].has_moved = True
    for piece in board.board_dict:
        assert piece in castled_board.board_dict
        assert board.board_dict[piece].x == castled_board.board_dict[piece].x
        assert board.board_dict[piece].y == castled_board.board_dict[piece].y
        assert board.board_dict[piece].colour == castled_board.board_dict[piece].colour
        assert board.board_dict[piece].has_moved == castled_board.board_dict[piece].has_moved
        assert board.board_dict[piece].letter == castled_board.board_dict[piece].letter


def test_promote():
    board = read_board("board_promotion_before.txt")
    board.promote((0, 0), "Q")
    promoted_board = read_board("board_promotion_after_to_queen.txt")
    for piece in board.board_dict:
        assert piece in promoted_board.board_dict
        assert board.board_dict[piece].x == promoted_board.board_dict[piece].x
        assert board.board_dict[piece].y == promoted_board.board_dict[piece].y
        assert board.board_dict[piece].colour == promoted_board.board_dict[piece].colour
        assert board.board_dict[piece].has_moved == promoted_board.board_dict[piece].has_moved
        assert board.board_dict[piece].letter == promoted_board.board_dict[piece].letter


def test_filter_moves():
    knight_pin_board = read_board("board_pinned_knight.txt")
    # testing generic filter_moves case
    filtered = knight_pin_board.filter_moves(knight_pin_board.board_dict[(
        2, 5)].get_valid_moves(knight_pin_board, "", None, None), (2, 5))
    assert filtered == []


def test_checkmate():
    scholars_mate_board = read_board("board_scholars_mate.txt")
    # print(scholars_mate_board.in_check(Colour.WHITE))
    assert scholars_mate_board.is_checkmate(Colour.WHITE) == True


def test_draw():
    # note that the only draw case that is here is stalemate
    stalemate_board = read_board("board_stalemate.txt")
    assert stalemate_board.is_draw(Colour.BLACK) == True
    assert stalemate_board.is_draw(Colour.WHITE) == False
