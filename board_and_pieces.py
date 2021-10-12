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

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple, include_castle_moves=False):
        x = self.x
        y = self.y
        all_squares = [(x+1, y-2), (x+2, y-1), (x+2, y+1), (x+1, y+2),
                       (x-1, y-2), (x-2, y-1), (x-1, y+2), (x-2, y+1)]
        # filter out moves that are not on the board
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

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple, include_castle_moves=False):
        return self.increment([(1, -1), (1, 1), (-1, 1), (-1, -1)], board)

    def deepcopy(self):
        return Bishop(self.x, self.y, self.colour, self.has_moved)


class Rook(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♖" if colour == Colour.BLACK else "♜"

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple, include_castle_moves=False):
        return self.increment([(1, 0), (0, 1), (-1, 0), (0, -1)], board)

    def deepcopy(self):
        return Rook(self.x, self.y, self.colour, self.has_moved)


class Queen(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♕" if colour == Colour.BLACK else "♛"

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple, include_castle_moves=False):
        return self.increment([(1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)], board)

    def deepcopy(self):
        return Queen(self.x, self.y, self.colour, self.has_moved)


class King(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♔" if colour == Colour.BLACK else "♚"

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple, include_castle_moves=False):
        x = self.x
        y = self.y

        moves_on_board = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y),
                          (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]

        possible_moves = [
            square for square in moves_on_board if self.on_board(square)]

        valid_moves = [move for move in possible_moves if (
            not move in board.board_dict) or (board.board_dict[move].colour != self.colour)]

        if not include_castle_moves:
            can_queenside, can_kingside = self.can_castle(board)
            if can_queenside:
                valid_moves.append(("Queenside",))
            if can_kingside:
                valid_moves.append(("Kingside",))

        return valid_moves

    def can_castle(self, board):
        # if king has moved return False
        if self.has_moved:
            return False, False

        queenside = True
        kingside = True
        rank = 0 if self.colour == Colour.BLACK else 7
        # if the queenside rook is no longer in its original place (captured or moved), or it moved but returned back there, or another piece is there instead, queenside castle is not possible
        if (not (0, rank) in board.board_dict) or board.board_dict[(0, rank)].has_moved:
            queenside = False
        # if the kingside rook is no longer in its original place (captured or moved), or it moved but returned back there, or another piece is there instead, kingside castle is not possible
        if (not (7, rank) in board.board_dict) or board.board_dict[(7, rank)].has_moved:
            kingside = False
        # if there are pieces in between king and queenside rook, then queenside castle is also not possible
        in_btwn_queenside = [(1, rank), (2, rank), (3, rank)]
        for square in in_btwn_queenside:
            if square in board.board_dict:
                queenside = False
        # if there are pieces in between king and kingside rook, then kingside castle is also not possible
        in_btwn_kingside = [(5, rank), (6, rank)]
        for square in in_btwn_kingside:
            if square in board.board_dict:
                kingside = False
        # for every opposing coloured piece, check if the squares in between the king and queenside rook (including the king) are in them
        # if they are, then queenside castle is not possible
        in_btwn_queenside.append((self.x, self.y))
        for piece in board.board_dict:
            if board.board_dict[piece].colour != self.colour:
                moves = board.board_dict[piece].get_valid_moves(
                    board, board.last_moved, board.initial_pos, board.final_pos, include_castle_moves=True)
                for square in in_btwn_queenside:
                    if square in moves:
                        queenside = False
        # for every opposing coloured piece, check if the squares in between the king and queenside rook (including the king) are in them
        # if they are, then queenside castle is not possible
        in_btwn_kingside.append((self.x, self.y))
        for piece in board.board_dict:
            if board.board_dict[piece].colour != self.colour:
                moves = board.board_dict[piece].get_valid_moves(
                    board, board.last_moved, board.initial_pos, board.final_pos, include_castle_moves=True)
                for square in in_btwn_kingside:
                    if square in moves:
                        kingside = False

        return queenside, kingside

    def deepcopy(self):
        return King(self.x, self.y, self.colour, self.has_moved)


class Pawn(Piece):
    def __init__(self, x: int, y: int, colour: Enum, has_moved=False):
        super().__init__(x, y, colour)
        self.letter = "♙" if colour == Colour.BLACK else "♟︎"
        self.direction_factor = 1 if colour == Colour.BLACK else -1

    def get_valid_moves(self, board, last_moved: str, initial_pos: tuple, final_pos: tuple, include_castle_moves=False):
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
                possible_moves.append((x+1, y + dir_factor, dir_factor))
            elif (x-1, y) == final_pos:
                possible_moves.append((x-1, y + dir_factor, dir_factor))
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
            self.board_dict[(3, 7)] = Queen(3, 7, Colour.WHITE)
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
            self.board_dict[(3, 0)] = Queen(3, 0, Colour.BLACK)
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

        return Board(board_dict=copy, last_moved=self.last_moved, initial_pos=self.initial_pos, final_pos=self.final_pos)

    def in_check(self, colour: Enum):
        # get king position of same colour
        letter = "♔" if colour == Colour.BLACK else "♚"
        king_posn = None
        for piece in self.board_dict:
            if self.board_dict[piece].letter == letter and self.board_dict[piece].colour == colour:
                king_posn = piece

        # get copy of board
        copy_board = self.deepcopy()
        # search for king's position in opposing colour pieces
        for piece in self.board_dict:
            if self.board_dict[piece].colour != colour and king_posn in self.board_dict[piece].get_valid_moves(copy_board, self.last_moved, self.initial_pos, self.final_pos, include_castle_moves=True):
                return True
        return False

    def make_move(self, piece_location: tuple, move_location: tuple) -> None:
        # regular move
        if len(move_location) == 2:
            moved_piece = self.board_dict[piece_location].deepcopy()
            del self.board_dict[piece_location]
            moved_piece.x = move_location[0]
            moved_piece.y = move_location[1]
            moved_piece.has_moved = True
            self.board_dict[move_location] = moved_piece
            # promote piece if moved piece is a pawn and it reached the end
            if (self.board_dict[move_location].letter == "♙" and move_location[1] == 7) or (self.board_dict[move_location].letter == "♟︎" and move_location[1] == 0):
                self.promote(move_location)
        # en passant 
        elif len(move_location) == 3:
            moved_piece = self.board_dict[piece_location].deepcopy()
            del self.board_dict[piece_location]
            delete_direction = move_location[2]
            del self.board_dict[(
                move_location[0], move_location[1] - delete_direction)]
            moved_piece.x = move_location[0]
            moved_piece.y = move_location[1]
            moved_piece.has_moved = True
            self.board_dict[(move_location[0], move_location[1])] = moved_piece
        # castling
        else:
            rank = 0 if self.board_dict[piece_location].colour == Colour.BLACK else 7
            if move_location[0] == "Queenside":
                queenside_rook_copy = self.board_dict[(0, rank)].deepcopy()
                king_copy = self.board_dict[piece_location].deepcopy()
                del self.board_dict[piece_location]
                del self.board_dict[(0, rank)]
                queenside_rook_copy.has_moved = True
                queenside_rook_copy.x = 3
                king_copy.has_moved = True
                king_copy.x = 2
                self.board_dict[(3, rank)] = queenside_rook_copy
                self.board_dict[(2, rank)] = king_copy
            else:
                kingside_rook_copy = self.board_dict[(7, rank)].deepcopy()
                king_copy = self.board_dict[piece_location].deepcopy()
                del self.board_dict[piece_location]
                del self.board_dict[(7, rank)]
                kingside_rook_copy.has_moved = True
                kingside_rook_copy.x = 5
                king_copy.has_moved = True
                king_copy.x = 6
                self.board_dict[(5, rank)] = kingside_rook_copy
                self.board_dict[(6, rank)] = king_copy
        self.last_moved = self.board_dict[(move_location[0], move_location[1])].letter if len(
            move_location) != 1 else "castle"
        self.initial_pos = piece_location
        self.final_pos = move_location
        return

    def promote(self, move_location: tuple, piece="") -> None:
        colour = self.board_dict[move_location].colour
        valid_choice = False if not piece else True
        while not valid_choice:
            piece = input("What piece would you like to promote to at " +
                          str(move_location) + " ?: ").upper()
            if piece == "Q" or piece == "R" or piece == "N" or piece == "B":
                valid_choice = True
            else:
                print("Invalid choice. Try again.")
        # set piece at move_location to the piece of choice
        if piece == "N":
            self.board_dict[move_location] = Knight(
                move_location[0], move_location[1], colour)
        elif piece == "B":
            self.board_dict[move_location] = Bishop(
                move_location[0], move_location[1], colour)
        elif piece == "R":
            self.board_dict[move_location] = Rook(
                move_location[0], move_location[1], colour)
        else:
            self.board_dict[move_location] = Queen(
                move_location[0], move_location[1], colour)
        return

    def filter_moves(self, moves_lst, piece_location):
        filtered = []
        colour = self.board_dict[piece_location].colour
        for move in moves_lst:
            temp_board = self.deepcopy()
            temp_board.make_move((piece_location[0], piece_location[1]), move)
            if not temp_board.in_check(colour):
                filtered.append(move)
        return filtered

    def is_checkmate(self, colour):
        copy_board = self.deepcopy()
        for piece in self.board_dict:
            if self.board_dict[piece].colour == colour:
                moves = self.filter_moves(self.board_dict[piece].get_valid_moves(
                    copy_board, self.last_moved, self.initial_pos, self.final_pos, include_castle_moves=True), (self.board_dict[piece].x, self.board_dict[piece].y))
                if len(moves) > 0:
                    return False
        if self.in_check(colour):
            return True
        return False

    def is_draw(self, colour):
        copy_board = self.deepcopy()
        for piece in self.board_dict:
            if self.board_dict[piece].colour == colour:
                moves = self.filter_moves(self.board_dict[piece].get_valid_moves(
                    copy_board, self.last_moved, self.initial_pos, self.final_pos, include_castle_moves=True), (self.board_dict[piece].x, self.board_dict[piece].y))
                if len(moves) > 0:
                    return False

        if not self.in_check(colour):
            return True

        return False
