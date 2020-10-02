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
        self.openColumns = np.arange(0, columnCount) #keeps track of columns that pieces can be dropped into
        self.winningBoard = False

    def __hash__(self):
        return hash(self.board)
    def __eq__(self, obj):
        return np.arrayequal(self.board, obj.board)
    def __str__(self):
        out = ""
        for row in self.board:
            for entry in row:
                if entry == 1:
                    out += " X "
                elif entry == 2:
                    out += " O "
                elif entry == 0:
                    out += " . "
            out += '\n'
        return out

    #check a given row for n in a row
    def _checkHorizontal(self, rowNum):
        amountInARow = 0
        for loc in self.board[rowNum]:
            if amountInARow == self.n:
                print("winner found in horizontal")
                return True
            if loc == self.player:
                amountInARow += 1
            else:
                amountInARow = 0
        return False
    
    #check a given column for n in a row
    def _checkVertical(self, colNum):
        amountInARow = 0
        for row in self.board:
            print(amountInARow)
            if amountInARow == self.n:
                print("winner found in vertical")
                return True
            if row[colNum] == self.player:
                amountInARow += 1
            else:
                amountInARow = 0
        return False
    
    #check diagonals of a piece given row and col numbers
    def _checkDiagonals(self, rowNum, colNum):
        amountInARow = 0
        #first get diagonal
        #figure out where to start tracing
        i = rowNum
        j = colNum 
        while i > 0 and j > 0:
            i -= 1
            j -= 1
        #then we trace along the diagonal
        while i < self.rowCount - 1 and j < self.columnCount - 1:
            if amountInARow == self.n:
                print("Winner found in diagonal")
                return True
            if self.board[i][j] == self.player:
                amountInARow += 1
            else:
                amountInARow = 0
            i += 1
            j += 1
        #get antidiagonal
        amountInARow = 0
        i = rowNum
        j = colNum 
        while i < self.rowCount - 1 and j > 0:
            i += 1
            j -= 1
        #trace along the antidiagonal
        while i > 0 and j < self.columnCount - 1:
            if amountInARow == self.n:
                print("Winner found in antidiagonal")
                return True
            if self.board[i][j] == self.player:
                amountInARow += 1
            else:
                amountInARow = 0
            i -= 1
            j += 1

        return False
                


    #meant to be called immediately after dropping a piece
    #given an index, determines whether newly dropped piece in this location is a win
    #returns true false-- is game state a win?
    def _isWin(self, row, column):
        #check horizontal
        if self._checkVertical(column) or self._checkHorizontal(row) or self._checkDiagonals(row, column):
            self.winningBoard = True
        else:
            self.winningBoard = False
        

        
    #columns for player are numbered 0-(columnCount-1)
    #row index of where piece is placed
    def _drop_piece(self, colNumber):
        rowOut = -1
        for i in range(self.rowCount):
            if self.board[i][colNumber] != 0:
                rowOut = i-1
                self.board[i-1][colNumber] = self.player
                #if i == 1, that means the column is now full; remove from open columns
                if i == 1:
                    self.openColumns = self.openColumns[self.openColumns != colNumber]
                    print(str(colNumber) + " removed from openColumns")
                    print(self.openColumns)
                return rowOut
        #if all of them are 0, drop to bottom
        self.board[self.rowCount-1][colNumber] = self.player
        return rowOut

    #returns 1 for a player 1 win; 2 for a player 2 win; 3 for a draw; 0 for game in progress; -1 for invalid move
    def player_move(self, columnNumber):
        if columnNumber in self.openColumns:
            rowNumber = self._drop_piece(columnNumber)
            #check to see if it's a winner
            self._isWin(rowNumber, columnNumber)
            if self.winningBoard:
                return self.player

            #if it's not a win, prepare for next round
            if self.player == 1:
                nextPlayer = 2
            elif self.player == 2:
                nextPlayer == 1
            return 0
        else:
            print("Column " + str(columnNumber) + " cannot be played")
            return -1 
        #TODO: then we need to return next possible game boards




def main():
    gameBoard = ConnectFourBoard(7, 6, 4)
    print(gameBoard)

    col = int(input("Enter a column to drop piece: "))
    play = gameBoard.player_move(col)
    print(gameBoard)
    while play == 0:
        col = int(input("Enter a column to drop piece: "))
        play = gameBoard.player_move(col)
        if play == 1:
            print("Win!")
        print(gameBoard)
        
    
    


    


main()