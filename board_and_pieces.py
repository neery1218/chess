
class Piece:
    def __init__(self, x: int, y: int, colour: str, letter: str) -> None:
        self.x = x
        self.y = y
        self.colour = colour
        self.letter = letter
        self.has_moved = False
    def on_board(self, x: int, y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

class Knight(Piece):
    def __init__(self, x: int, y: int, colour: str, letter: str) -> None:
        Piece.__init__(self, x, y, colour, letter)

class Bishop(Piece):
    def __init__(self, x: int, y: int, colour: str, letter: str) -> None:
        Piece.__init__(self, x, y, colour, letter)

class Rook(Piece):
    def __init__(self, x: int, y: int, colour: str, letter: str) -> None:
        Piece.__init__(self, x, y, colour, letter)

class Queen(Piece):
    def __init__(self, x: int, y: int, colour: str, letter: str) -> None:
        Piece.__init__(self, x, y, colour, letter)

class King(Piece):
    def __init__(self, x: int, y: int, colour: str, letter: str) -> None:
        Piece.__init__(self, x, y, colour, letter)

class Pawn(Piece):
    def __init__(self, x: int, y: int, colour: str, letter: str) -> None:
        Piece.__init__(self, x, y, colour, letter)

        
class Board:
    def __init__(self, board_dict = {}) -> None:
        self.board_dict = {}
        if len(board_dict) == 0:
            #WHITE PIECES
            #set white pawns
            for x in range(8):
                self.board_dict[(x, 6)] = Pawn(x, 6, "White", "P")
            #set white king
            self.board_dict[(4,7)] = King(4, 7, "White", "K")
            #set white queen
            self.board_dict[(3,7)] = Queen(4, 7, "White", "Q")
            #set white rooks
            self.board_dict[(0,7)] = Rook(0, 7, "White", "R")
            self.board_dict[(7,7)] = Rook(0, 7, "White", "R")
            #set white bishops
            self.board_dict[(2,7)] = Bishop(2, 7, "White", "B")
            self.board_dict[(5,7)] = Bishop(5, 7, "White", "B")
            #set white knights
            self.board_dict[(1,7)] = Knight(1, 7, "White", "K")
            self.board_dict[(6,7)] = Knight(6, 7, "White", "K")
            #BLACK PIECES
            #set black pawns
            for x in range(8):
                self.board_dict[(x, 1)] = Pawn(x, 1, "Black", "p")
            #set black king
            self.board_dict[(4,0)] = King(4, 0, "Black", "k")
            #set black queen
            self.board_dict[(3,0)] = Queen(4, 0, "Black", "q")
            #set black rooks
            self.board_dict[(0,0)] = Rook(0, 0, "Black", "r")
            self.board_dict[(7,0)] = Rook(7, 0, "Black", "r")
            #set black bishops
            self.board_dict[(2,0)] = Bishop(2, 0, "Black", "b")
            self.board_dict[(5,0)] = Bishop(5, 0, "Black", "b")
            #set black knights
            self.board_dict[(1,0)] = Knight(1, 0, "Black", "k")
            self.board_dict[(6,0)] = Knight(6, 0, "Black", "k")
        return
    
    def print(self) -> None:
        s = " "
        for y in range(8):
            arr = []
            for x in range(8):
                if (x,y) in self.board_dict:
                    arr.append(self.board_dict[(x,y)].letter)
                else:
                    arr.append("-")
            print(s.join(arr))
        return

board = Board()
board.print()