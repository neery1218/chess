from board_and_pieces import *

board = Board()
game_over = False
whites_turn = True
is_draw = False
is_checkmate = False

while not game_over:
    print(board)
    to_move = "\nWhite to move\n-------------\n" if whites_turn else "\nBlack to move\n-------------\n"
    print(to_move)
    # get input and check if valid piece is selected
    valid_piece = False
    while not valid_piece:
        y = int(input("Enter row of piece you want to move: "))
        x = int(input("Enter column of piece you want to move: "))
        if (x, y) in board.board_dict and ((whites_turn and board.board_dict[(x, y)].colour == Colour.WHITE) or (not whites_turn and board.board_dict[(x, y)].colour == Colour.BLACK)) and len(board.filter_moves(board.board_dict[(x, y)].get_valid_moves(board, board.last_moved, board.initial_pos, board.final_pos), (x, y))) > 0:
            valid_piece = True
        else:
            print("Invalid piece selected. Try again. ")

    moves = board.filter_moves(board.board_dict[(x, y)].get_valid_moves(
        board, board.last_moved, board.initial_pos, board.final_pos), (x, y))

    print(moves)

    # get move location

    valid_move = False
    index = None
    while not valid_move:
        index = int(
            input("Enter index of moves list above that you would like to move to: "))
        if 0 <= index < len(moves):
            valid_move = True
        else:
            print("Invalid move index. Try again.")

    board.make_move((x, y), moves[index])

    colour = Colour.BLACK if whites_turn else Colour.WHITE

    if board.is_draw(colour):
        is_draw = True
        game_over = True
        break
    if board.is_checkmate(colour):
        is_checkmate = True
        game_over = True
        break

    whites_turn = not whites_turn

print(board)
if is_draw:
    print("Stalemate. No one wins.")

if is_checkmate:
    colour = "White" if whites_turn else "Black"
    print("Checkmate. " + colour + " wins.")
