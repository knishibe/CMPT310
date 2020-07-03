# a3.py

# ...

import random 
import time

# this function starts a new game of tic tac toe with the computer
def play_a_new_game():

    # initialize new game
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    valid_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    count = 0
    win = False
    draw = False
    random.seed()

    while True:
        # allow player to choose X or O (first or second)
        val = input("Would you like to be X or O? (X goes first): ")
        print("\n", end="")
        if val.lower() == 'x':
            human = 1
            computer = 2
            break
        elif val.lower() == 'o':
            human = 2
            computer = 1
            break
        else:
            print("Error: Invalid  input, please try again\n")

    # continue game until someone has won or there is a draw
    while not win and not draw:
        print_board(board)

        # alternate players
        player = (count % 2) + 1
        count += 1
        print("Player %d's turn\n" %player)

        # select valid move
        if player == human:
            move = humanTurn(valid_moves)
        else:
            move = computerTurn(board, valid_moves, computer)

        # update the board with the chosen move with the 
        # current player's token
        board[move] = player
        valid_moves.remove(move)

        # check if the game is complete
        win = check_win(board, player)
        draw = check_draw(board)

    print_board(board)

    if win:
        print("\nPlayer %d won!" %player)
    elif draw:
        print("\nDraw!")


# this function is to allow the player to take their turn
def humanTurn(valid_moves):
    while True:
        print("Valid moves: ", valid_moves)
        val = input("Please enter the box that you would like to go: ")
        print("\n", end="")
        move = int(val)
        if move in valid_moves:
            return move
        print("Error: Invalid  move, please try again\n")

# this function is to allow the computer to take it's turn
# using the pure monte carlo tree search algorithm
def computerTurn(board, valid_moves, computer):
    h_val = {}

    # if only one move is possible, do that move
    if len(valid_moves) == 1:
        return int(valid_moves[0])

    # for each valid move do random playouts
    for i in range(len(valid_moves)):

        move = valid_moves[i]
        h_val[str(move)] = 0
        wins = 0
        losses = 0
        draws = 0

        # complete 500 random playouts for each valid move
        for j in range(150):
            win = False
            draw = False
            test_board = board.copy();
            test_board[move] = computer
            count = computer
            valid_test_moves = valid_moves.copy()
            valid_test_moves.remove(move)

            # continue playout until someone wins or there is a draw
            while not win and not draw:
                player = (count % 2) + 1 
                count += 1
                test_move = random.choice(valid_test_moves)
                valid_test_moves.remove(test_move)
                test_board[test_move] = player
                win = check_win(test_board, player)
                draw = check_draw(test_board)

            # heuristic: increment for win, decrement for loss and do nothing for draw
            if win and player == computer:
                wins += 1
            elif win and player != computer:
                losses += 1
            elif draw:
                draws += 1
        
        if computer == 1:
            h_val[str(move)] = -losses
        elif computer == 2:
            h_val[str(move)] = wins - losses

    # select the move with the highest heuristic value
    comp_move = max(h_val, key=h_val.get)
    return int(comp_move)

# this function is to determine if there is a draw
def check_draw(board):
    # draw if all spaces filled 
    if 0 not in board:
        return True
    else:
        return False

# this function is to determine whether or not a 
# certain player has won the game
def check_win(board, player):

    # check horizontal lines
    for i in range(3):
        if board[i*3] == player and board[1+i*3] == player and board[2+i*3] == player:
            return True

    # check vertical lines
    for i in range(3):
        if board[i] == player and board[3+i] == player and board[6+i] == player:
            return True

    # check diagonal lines
    if ((board[0] == player and board[4] == player and board[8] == player) or 
        (board[2] == player and board[4] == player and board[6] == player)): 
        return True

    return False


# this function is used to print the current
# tic tac toe board to console
def print_board(board):

    # player 1 is X player 2 is O
    for i in range(3):
        for j in range(3):
            if board[i*3+j] == 0:
                print(" * ", end = "")
            elif board[i*3+j] == 1:
                print(" X ", end = "")
            elif board[i*3+j] == 2:
                print(" O ", end = "")

            # print lines in board
            if j != 2:
                print("|", end = "")
        if i != 2:
            print("\n---+---+---")
    print("\n")


if __name__ == '__main__':
    play_a_new_game()
