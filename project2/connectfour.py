import numpy as np
#class depicting a connect four board
class ConnectFourBoard():
    #n is number of pieces in a row required to win
    def __init__(self, columnCount, rowCount, n):
        self.columnCount = columnCount
        self.rowCount = rowCount
        self.n = n
        self.board = np.zeros((rowCount, columnCount))
        self.player = 1 #player 1 starts

    #TODO: __hash__() so class works in dictionary
    #TODO: __equals__() so class works in dictionary
    
    #columns for player are numbered 0-(columnCount-1)
    def _drop_piece(self, playerNum, colNumber):
        #first, make sure that column isn't full (valid move)
        if self.board[0][colNumber] == 0:
            for i in range(self.rowCount):
                if self.board[i][colNumber] != 0:
                    self.board[i-1][colNumber] = playerNum
                    return True
            #if all of them are 0, drop to bottom
            self.board[self.rowCount-1][colNumber] = playerNum
            return True
        else:
            return False

    #human player will always be player 1, so 
    def player_move(self, playerNum):
        validMove = False
        colNum = input("Player, choose a column to drop a piece: ")
        validMove = self._drop_piece(playerNum, colNum)

        while not validMove:
            print("Invalid column chosen. The selected column is already full. Try again.")
            colNum = input("Player, choose a column to drop a piece: ")
            validMove = self._drop_piece(playerNum, colNum)
        
        #TODO: check to see if its a win
        self.whosTurnIsIt = 2 #AI's turn

    #given the coordinates of a piece, sees if there is a winning sequence with this piece
    def isWin(self):

        

    def print_board(self):
        for i in range(self.rowCount):
            print(self.board[i])
        print('\n')



def main():
    gameBoard = ConnectFourBoard(7, 6, 4)

    gameBoard.drop_piece(1, 0)

    gameBoard.print_board()

    gameBoard.drop_piece(2, 0)
    gameBoard.print_board()

    gameBoard.drop_piece(1, 3)
    gameBoard.print_board()


main()