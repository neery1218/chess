from enum import Enum


class Colour(Enum):
    WHITE = 1
    BLACK = 2


class Piece:
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False) -> None:
        self.x = x
        self.y = y
        self.colour = colour
        self.has_moved = has_moved

    def on_board(self, pos: tuple) -> bool:
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8

    def increment(self, increment_lst, board):
        possible_moves = []
        x = self.x
        y = self.y
        for x_inc, y_inc in increment_lst:
            for i in range(8):
                print((x+x_inc*(i+1), y+y_inc*(i+1)))
                if not self.on_board((x+x_inc*(i+1), y+y_inc*(i+1))):
                    break
                elif (x+x_inc*(i+1), y+y_inc*(i+1)) in board.board_dict:
                    if board.board_dict[(x+x_inc*(i+1), y+y_inc*(i+1))].colour != self.colour:
                        possible_moves.append((x+x_inc*(i+1), y+y_inc*(i+1)))
                    break
                else:
                    possible_moves.append((x+x_inc*(i+1), y+y_inc*(i+1)))
        return possible_moves


class Knight(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♘" if colour == Colour.BLACK else "♞"

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple):
        x = self.x
        y = self.y
        all_squares = [(x+1, y-2), (x+2, y-1), (x+2, y+1), (x+1, y+2),
                       (x-1, y-2), (x-2, y-1), (x-1, y+2), (x-2, y+1)]
        # filter out moves that are not even on the board
        moves_on_board = [
            square for square in all_squares if self.on_board(square)]

        valid_moves = [move for move in moves_on_board if (
            not move in board.board_dict) or (board.board_dict[move].colour != self.colour)]

        return valid_moves

    def deepcopy(self):
        return Knight(self.x, self.y, self.colour, self.has_moved)


class Bishop(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♗" if colour == Colour.BLACK else "♝"

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple):
        return self.increment([(1, -1), (1, 1), (-1, 1), (-1, -1)], board)

    def deepcopy(self):
        return Bishop(self.x, self.y, self.colour, self.has_moved)


class Rook(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♖" if colour == Colour.BLACK else "♜"

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple):
        return self.increment([(1, 0), (0, 1), (-1, 0), (0, -1)], board)

    def deepcopy(self):
        return Rook(self.x, self.y, self.colour, self.has_moved)


class Queen(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♕" if colour == Colour.BLACK else "♛"

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple):
        return self.increment([(1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)], board)

    def deepcopy(self):
        return Queen(self.x, self.y, self.colour, self.has_moved)


class King(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♔" if colour == Colour.BLACK else "♚"

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple):
        x = self.x
        y = self.y

        all_squares = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y),
                       (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]
        possible_moves = [
            square for square in all_squares if self.on_board(square)]
        return possible_moves

    def deepcopy(self):
        return King(self.x, self.y, self.colour, self.has_moved)


class Pawn(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♙" if colour == Colour.BLACK else "♟︎"
        self.direction_factor = 1 if colour == Colour.BLACK else -1

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple):
        x = self.x
        y = self.y
        dir_factor = self.direction_factor
        possible_moves = []
        # forward squares (2 squares and 1 square)
        if not self.has_moved and not (x, y + 2*dir_factor) in board.board_dict and not (x, y + dir_factor) in board.board_dict:
            possible_moves.append((x, y + 2*dir_factor))
        if not (x, y + dir_factor) in board.board_dict:
            possible_moves.append((x, y + dir_factor))
        # diagonal squares (x+1, y + dir_factor)
        # Case 1: Diagonal square has opposing colour piece
        if (x+1, y + dir_factor) in board.board_dict and board.board_dict[(x+1, y + dir_factor)].colour != self.colour:
            possible_moves.append((x+1, y + dir_factor))
        if (x-1, y + dir_factor) in board.board_dict and board.board_dict[(x-1, y + dir_factor)].colour != self.colour:
            possible_moves.append((x-1, y + dir_factor))
        # Case 2: En passant
        if (last_moved == "♙" or last_moved == "♟︎") and abs(final_pos[1] - initial_pos[1]) == 2:
            if (x+1, y) == final_pos:
                possible_moves.append((x+1, y + dir_factor, "en passant"))
            elif (x-1, y) == final_pos:
                possible_moves.append((x-1, y + dir_factor, "en passant"))
        return possible_moves

    def deepcopy(self):
        return Pawn(self.x, self.y, self.colour, self.has_moved)


class Board:
    def __init__(self, board_dict={}, last_moved=None, initial_pos=None, final_pos=None) -> None:
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
        
        self.last_moved = last_moved
        self.initial_pos = initial_pos
        self.final_pos = final_pos

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

    def deepcopy(self):
        copy = {}
        
        for piece in self.board_dict:
            copy[(piece[0], piece[1])] = self.board_dict[piece].deepcopy()

        return Board(board_dict = copy, last_moved = self.last_moved, initial_pos = self.initial_pos, final_pos = self.final_pos)

    
    def in_check(self, colour: Enum):
        # get king position of same colour
        letter = "♔" if colour == Colour.BLACK else "♚"
        king_posn = None
        for piece in self.board_dict:
            if self.board_dict[piece].letter == letter and self.board_dict[piece].colour == colour:
                king_posn = piece

        #get copy of board
        copy_board = self.deepcopy()
        #search for king's position in opposing colour pieces
        for piece in self.board_dict:
            if self.board_dict[piece].colour != colour and king_posn in self.board_dict[piece].get_valid_moves(copy_board, self.last_moved, self.initial_pos, self.final_pos):
                return True
        return False




