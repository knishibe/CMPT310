## a3.py
import random

WINS = 0 
LOSSES = 0
TIES = 0

#====================================================================================================================
# Tic-Tac-Toe class
class TicTacToe:
    def __init__(self):
        self.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.turn = None # Computer = 'C', User = 'U'
        self.terminate = False # Game is complete
        self.first = None
        
        choice = None
        while choice != "yes" and choice != "no":
            choice = input("Would you like to go first? (yes/no): ")
            print("\n")
            if choice == "yes":
                self.turn = 'U'
                self.first = 'U'
            elif choice == "no":
                self.turn = 'C'
                self.first = 'C'

    def displayBoard(self):
        for i, tile in enumerate(self.board):
            if (i+1)%3 == 0 or i==8:
                tile = str(tile)
                print("%2s"%(tile))
                if i!=8:
                    print("--+--+--")
            else:
                print("%2s|"%(tile),end='')
        print("\n")
        return None

    def whoseTurn(self):
        return self.turn

    # Display a readable interface with numbered tiles for user to choose a move 
    def showPossibleMoves(self):
        print("The numbered tiles below are the possible choices.\n")
        for i, tile in enumerate(self.board):
            if (i+1)%3 == 0 or i==8:
                tile = str(tile)
                if tile == "O" or tile == "X":
                    print("%2s"%(tile))
                else:
                    print("%2d"%(i+1))
                if i!=8:
                    print("--+--+--")
            else:
                if tile == "O" or tile == "X":
                    print("%2s|"%(tile),end='')
                else:
                     print("%2d|"%(i+1),end='')
        print("\n")
        return None

    def makeMove(self, choice): # choice is [1,9]
        if self.turn == 'C':
            self.board[int(choice)-1]='O'
            if self.checkWin(int(choice)-1, None):
                self.displayBoard()
                print("Computer Wins!\n")
                self.terminate = True
                global WINS
                WINS +=1
        else:
            self.board[int(choice)-1]='X'
            if self.checkWin(int(choice)-1, None):
                self.displayBoard()
                print("You Win!\n")
                self.terminate = True
                global LOSSES
                LOSSES +=1
        
        # Board is filled
        if not self.terminate and not self.getPossibleMoves(None):
            print("Draw!\n")
            self.terminate = True
            global TIES
            TIES +=1
        return None

    def checkWin(self, position, sim_board):
        if sim_board == None:
            board = self.board
        else:
            board = sim_board
        if position == 0: # array index
            if board[position] == board[1] and board[position] == board[2] \
                or (board[position] == board[3] and board[position] == board[6]) \
                or (board[position] == board[4] and board[position] == board[8]):
                    return True
        if position == 1: 
            if board[position] == board[0] and board[position] == board[2] \
                or (board[position] == board[4] and board[position] == board[7]):
                    return True
        if position == 2: 
            if board[position] == board[0] and board[position] == board[1] \
                or (board[position] == board[4] and board[position] == board[6]) \
                or (board[position] == board[5] and board[position] == board[8]):
                    return True
        if position == 3: 
            if board[position] == board[0] and board[position] == board[6] \
                or (board[position] == board[4] and board[position] == board[5]):
                    return True
        if position == 4: 
            if board[position] == board[0] and board[position] == board[8] \
                or (board[position] == board[2] and board[position] == board[6]) \
                or (board[position] == board[3] and board[position] == board[5]) \
                or (board[position] == board[1] and board[position] == board[7]):
                    return True
        if position == 5: 
            if board[position] == board[3] and board[position] == board[4] \
                or (board[position] == board[2] and board[position] == board[8]):
                    return True
        if position == 6: 
            if board[position] == board[0] and board[position] == board[3] \
                or (board[position] == board[2] and board[position] == board[4]) \
                or (board[position] == board[7] and board[position] == board[8]):
                    return True
        if position == 7: 
            if board[position] == board[1] and board[position] == board[4] \
                or (board[position] == board[6] and board[position] == board[8]):
                    return True
        if position == 8: 
            if board[position] == board[0] and board[position] == board[4] \
                or (board[position] == board[2] and board[position] == board[5]) \
                or (board[position] == board[6] and board[position] == board[7]):
                    return True
        return False

    def usersTurn(self):
        self.showPossibleMoves()
        moves = self.getPossibleMoves(None)
        choice = input("It's your turn. Input the number corresponding to your choice of tile placement: ")

        while (not choice or not choice.isdigit()):
            if not choice.isdigit():
                choice = input("Invalid move. Input the number corresponding to your choice of tile placement: ")
            elif int(choice)-1 not in moves:
                choice = input("Invalid move. Input the number corresponding to your choice of tile placement: ")

        print('\n')
        self.makeMove(choice)
        self.displayBoard()
        self.turn = 'C'

    def computersTurn(self):
        print("Opponent's deciding...\n")
        results = dict()
        index = 0
        # offensive
        if self.first == 'C':
            for i, tile in enumerate(self.board):
                if tile == ' ':
                    result = self.doRandomPlayouts(i) # [W, T, L]
                    results[i] = result[2]
            index = min(results, key=results.get)
                    
        # defensive
        else:
            for i, tile in enumerate(self.board):
                if tile == ' ':
                    result = self.doRandomPlayouts(i) # [W, T, L]
                    results[i] = result[0]+result[1]-10*result[2]
            index = max(results, key=results.get)
        self.makeMove(index+1) # map true index to a tile 1-9
        self.displayBoard()
        self.turn = 'U'

    # Do a number of random playouts where the computer simulates playing the game until 
    # it is over by making random moves for each player until a win, loss, or draw is reached. When a playout is done, 
    # the result (win, loss, or draw) is recorded, and then some more random playouts are done. After random playouts 
    # are done for all legal moves, it choses the move that results in ___________________________
    def doRandomPlayouts(self,pos):
        wins = 0
        ties = 0
        losts = 0

        for i in range(300):
            sim_board = self.board[:] #copy list
            sim_board[pos] = 'O'
            p = 'U'
            moves = self.getPossibleMoves(sim_board)
            w = False
            while moves:
                nextMove = random.choice(moves)
                if p == 'C':
                    sim_board[nextMove] = 'O'
                else:
                    sim_board[nextMove] = 'X'
                
                w = self.checkWin(nextMove, sim_board)
                if w and p == 'C':
                    wins+=1
                    break
                elif w and p == 'U':
                    losts+=1
                    break

                # Switch Player
                if p == 'C':
                    p = 'U'
                else:
                    p = 'C'

                moves = self.getPossibleMoves(sim_board)
        
            # if it's not a win and there are no more moves left
            if not w and len(moves) == 0:
                ties+=1
        return [wins,ties,losts]

    def getPossibleMoves(self, sim_board):
        if sim_board == None:
            board = self.board
        else:
            board = sim_board
        moves = []
        for i, tile in enumerate(board):
            if board[i] == ' ':
                moves.append(i)
        return moves

#====================================================================================================================
def play_a_new_game():
    replay = True
    while replay:
        game = TicTacToe()
        while not game.terminate:
            if game.whoseTurn() == 'U':
                game.usersTurn()
            else:
                game.computersTurn()

        choice = input("Would you like to play another game? Enter 'yes' to replay or any character to exit:  ")
        if choice != "yes":
            replay = False
        print("\n")

if __name__ == '__main__':
    play_a_new_game()
