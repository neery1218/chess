from enum import Enum

class Colour(Enum):
    WHITE = 1
    BLACK = 2

class Piece:
    def __init__(self, x: int, y: int, colour: Enum, letter: str) -> None:
        self.x = x
        self.y = y
        self.colour = colour
        self.letter = letter
        self.has_moved = False

    def on_board(self, x: int, y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

class Knight(Piece):
    pass


class Bishop(Piece):
    pass


class Rook(Piece):
    pass


class Queen(Piece):
    pass


class King(Piece):
    pass


class Pawn(Piece):
    pass

class Board:
    def __init__(self, board_dict={}) -> None:
        self.board_dict = {}
        if len(board_dict) == 0:
            # WHITE PIECES
            # set white pawns
            for x in range(8):
                self.board_dict[(x, 6)] = Pawn(x, 6, Colour.WHITE, "P")
            # set white king
            self.board_dict[(4, 7)] = King(4, 7, Colour.WHITE, "K")
            # set white queen
            self.board_dict[(3, 7)] = Queen(4, 7, Colour.WHITE, "Q")
            # set white rooks
            self.board_dict[(0, 7)] = Rook(0, 7, Colour.WHITE, "R")
            self.board_dict[(7, 7)] = Rook(0, 7, Colour.WHITE, "R")
            # set white bishops
            self.board_dict[(2, 7)] = Bishop(2, 7, Colour.WHITE, "B")
            self.board_dict[(5, 7)] = Bishop(5, 7, Colour.WHITE, "B")
            # set white knights
            self.board_dict[(1, 7)] = Knight(1, 7, Colour.WHITE, "K")
            self.board_dict[(6, 7)] = Knight(6, 7, Colour.WHITE, "K")
            # BLACK PIECES
            # set black pawns
            for x in range(8):
                self.board_dict[(x, 1)] = Pawn(x, 1, Colour.BLACK, "p")
            # set black king
            self.board_dict[(4, 0)] = King(4, 0, Colour.BLACK, "k")
            # set black queen
            self.board_dict[(3, 0)] = Queen(4, 0, Colour.BLACK, "q")
            # set black rooks
            self.board_dict[(0, 0)] = Rook(0, 0, Colour.BLACK, "r")
            self.board_dict[(7, 0)] = Rook(7, 0, Colour.BLACK, "r")
            # set black bishops
            self.board_dict[(2, 0)] = Bishop(2, 0, Colour.BLACK, "b")
            self.board_dict[(5, 0)] = Bishop(5, 0, Colour.BLACK, "b")
            # set black knights
            self.board_dict[(1, 0)] = Knight(1, 0, Colour.BLACK, "k")
            self.board_dict[(6, 0)] = Knight(6, 0, Colour.BLACK, "k")
        else:
            self.board_dict = board_dict

    def __str__(self) -> None:
        for y in range(8):
            arr = []
            for x in range(8):
                if (x, y) in self.board_dict:
                    arr.append(self.board_dict[(x, y)].letter)
                else:
                    arr.append("-")
            print(" ".join(arr))
        return
 