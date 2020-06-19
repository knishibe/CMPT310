# a3.py

# ...


def play_a_new_game():
    board = [[0, 0, 1], [0, 1, 2], [1, 2, 2]]
    count = 0
    win = False
    draw = False

    while not win and not draw:
        print_board(board)
        player = (count % 2) + 1 
        count += 1
        print("\n\nPlayer %d's turn\n\n" %player)
        #turn(board, player)
        win = check_win(board, player)
        #draw = check_draw(draw)

    print_board(board)

    if win:
        print("\n\nPlayer %d won!" %player)
    elif draw:
        print("\n\nDraw!")



#def turn(board, player):

#def check_draw(board):

def check_win(board, player):
    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            return True

    for i in range(3):
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            return True

    if ((board[0][0] == player and board[1][1] == player and board[2][2] == player) or 
        (board[0][2] == player and board[1][1] == player and board[2][0] == player)): 
        return True

    return False


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                print(" * ", end = "")
            elif board[i][j] == 1:
                print(" X ", end = "")
            elif board[i][j] == 2:
                print(" O ", end = "")

            if j != len(board[i]) - 1:
                print("|", end = "")
        if i != len(board) - 1:
            print("\n___________\n")


if __name__ == '__main__':
    play_a_new_game()
