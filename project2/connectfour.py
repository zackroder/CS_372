import numpy as np
#class depicting a connect four board
class ConnectFourBoard():
    #n is number of pieces in a row required to win
    def __init__(self, columnCount, rowCount, n, player=1, openColumns=None, board = None, movesExecuted = None):
        self.columnCount = columnCount
        self.rowCount = rowCount
        self.n = n
        if board is None:
            self.board = np.zeros((rowCount, columnCount))
        else:
            self.board = board
        
        self.player = player #player 1 starts

        if openColumns is None:
            self.openColumns = np.arange(0, columnCount)
        else:
            self.openColumns = openColumns #keeps track of columns that pieces can be dropped into
        
        self.winningBoard = False

        if movesExecuted is None:
            self.movesExecuted = 0
        else:
            self.movesExecuted = movesExecuted

    def __hash__(self):
        return hash(self.board)
    def __eq__(self, obj):
        return np.arrayequal(self.board, obj.board)
    def __neq__(self, obj):
        return not(self == obj)
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

    def get_board(self):
        return self.board
    def get_player(self):
        return self.player
    def get_columnCount(self):
        return self.columnCount
    def get_rowCount(self):
        return self.rowCount
    def get_n(self):
        return self.n
    def get_openColumns(self):
        return self.openColumns
    def get_movesExecuted(self):
        return self.movesExecuted

    #check a given row for n in a row
    def _checkHorizontal(self, rowNum):
        amountInARow = 0
        for loc in self.board[rowNum]:
            if loc == self.player:
                amountInARow += 1
                if amountInARow == self.n:
                    print("winner found in horizontal")
                    return True
            else:
                amountInARow = 0
        return False
    
    #check a given column for n in a row
    def _checkVertical(self, colNum):
        amountInARow = 0
        for row in self.board:
            if row[colNum] == self.player:
                amountInARow += 1
                if amountInARow == self.n:
                    print("winner found in vertical")
                    return True
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
    def isWin(self, row, column):
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
            #switch player number
            if self.player == 1:
                self.player = 2
            elif self.player == 2:
                self.player = 1
            
            #increase numbed of moves executed
            self.movesExecuted += 1
            #check to see if it's a winner
            self.isWin(rowNumber, columnNumber)
            if self.winningBoard:
                return self.player


            #if it's not a win, prepare for next round
            return 0
        else:
            print("Column " + str(columnNumber) + " cannot be played")
            return -1 

    #returns boolean T/F whether board is a terminal state (win or draw)
    def terminal_test(self):
        #if it's a win or game board is full w/o win (draw)
        if self.winningBoard or np.count_nonzero(self.board) == board.size :
            return True
        
        else:
            return False



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
        
    
    