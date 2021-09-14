from enum import Enum

class Colour(Enum):
    WHITE = 1
    BLACK = 2

class Piece:
    def __init__(self, x: int, y: int, colour: Enum) -> None:
        self.x = x
        self.y = y
        self.colour = colour
        self.has_moved = False

    def on_board(self, x: int, y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

class Knight(Piece):
    def __init__(self, x: int, y: int, colour: Enum):
        super().__init__(x, y, colour)
        self.letter = "N" if colour == Colour.WHITE else "n"


class Bishop(Piece):
    def __init__(self, x: int, y: int, colour: Enum):
        super().__init__(x, y, colour)
        self.letter = "B" if colour == Colour.WHITE else "b"


class Rook(Piece):
    def __init__(self, x: int, y: int, colour: Enum):
        super().__init__(x, y, colour)
        self.letter = "R" if colour == Colour.WHITE else "r"


class Queen(Piece):
    def __init__(self, x: int, y: int, colour: Enum):
        super().__init__(x, y, colour)
        self.letter = "Q" if colour == Colour.WHITE else "q"


class King(Piece):
    def __init__(self, x: int, y: int, colour: Enum):
        super().__init__(x, y, colour)
        self.letter = "K" if colour == Colour.WHITE else "k"


class Pawn(Piece):
    def __init__(self, x: int, y: int, colour: Enum):
        super().__init__(x, y, colour)
        self.letter = "P" if colour == Colour.WHITE else "p"

class Board:
    def __init__(self, board_dict={}) -> None:
        self.board_dict = {}
        if len(board_dict) == 0:
            # WHITE PIECES
            # set white pawns
            for x in range(8):
                self.board_dict[(x, 6)] = Pawn(x, 6, Colour.WHITE)
            # set white king
            self.board_dict[(4, 7)] = King(4, 7, Colour.WHITE)
            # set white queen
            self.board_dict[(3, 7)] = Queen(4, 7, Colour.WHITE)
            # set white rooks
            self.board_dict[(0, 7)] = Rook(0, 7, Colour.WHITE)
            self.board_dict[(7, 7)] = Rook(0, 7, Colour.WHITE)
            # set white bishops
            self.board_dict[(2, 7)] = Bishop(2, 7, Colour.WHITE)
            self.board_dict[(5, 7)] = Bishop(5, 7, Colour.WHITE)
            # set white knights
            self.board_dict[(1, 7)] = Knight(1, 7, Colour.WHITE)
            self.board_dict[(6, 7)] = Knight(6, 7, Colour.WHITE)
            # BLACK PIECES
            # set black pawns
            for x in range(8):
                self.board_dict[(x, 1)] = Pawn(x, 1, Colour.BLACK)
            # set black king
            self.board_dict[(4, 0)] = King(4, 0, Colour.BLACK)
            # set black queen
            self.board_dict[(3, 0)] = Queen(4, 0, Colour.BLACK)
            # set black rooks
            self.board_dict[(0, 0)] = Rook(0, 0, Colour.BLACK)
            self.board_dict[(7, 0)] = Rook(7, 0, Colour.BLACK)
            # set black bishops
            self.board_dict[(2, 0)] = Bishop(2, 0, Colour.BLACK)
            self.board_dict[(5, 0)] = Bishop(5, 0, Colour.BLACK)
            # set black knights
            self.board_dict[(1, 0)] = Knight(1, 0, Colour.BLACK)
            self.board_dict[(6, 0)] = Knight(6, 0, Colour.BLACK)
        else:
            self.board_dict = board_dict

    def __str__(self) -> None:
        s = ""
        for y in range(8):
            arr = []
            for x in range(8):
                if (x, y) in self.board_dict:
                    arr.append(self.board_dict[(x, y)].letter)
                else:
                    arr.append("-")
            s += " ".join(arr) + "\n"
        return s
 