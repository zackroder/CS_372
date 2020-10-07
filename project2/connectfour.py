import numpy as np
import copy


#class depicting a connect four board
class ConnectFourBoard():
    #n is number of pieces in a row required to win
    def __init__(self, columnCount, rowCount, n, player=1.0, openColumns=None, board = None, movesExecuted = None, lastMove = None):
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

        #last move stores coordinates of last move (col, row)
        if lastMove is None:
            self.lastMove = (None, None)
        else:
            self.lastMove = lastMove

    def __hash__(self):
        return hash(self.board.tostring())
    def __eq__(self, obj):
        return np.array_equal(self.board, obj.board)
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

    def swap_player(self):
        self.player = (1.0 if self.player == 2.0 else 2.0)

    #TODO fix this
    #check a given row for n in a row
    def _checkHorizontal(self, rowNum):
        amountInARow = 0
        #print("Row analyzed " + str(self.board[rowNum]))
        for loc in self.board[rowNum]:
            if loc == self.player:
                amountInARow += 1
                if amountInARow == self.n:
                    #print("winner found in horizontal")
                    return True
            else:
                amountInARow = 0
        return False
    
    #check a given column for n in a row
    def _checkVertical(self, colNum):
        amountInARow = 0
        col = []
        for row in self.board:
            if row[colNum] == self.player:
                amountInARow += 1
                if amountInARow == self.n:
                    #print("winner found in vertical")
                    return True
            else:
                amountInARow = 0
        #print("analyzed col " + str(col))
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
        
        diag = []
        #then we trace along the diagonal
        #print("start diag trace: " + str(i) + " " + str(j))
        while amountInARow != self.n and i < self.rowCount and j < self.columnCount:
            diag.append(self.board[i][j])
            if self.board[i][j] == self.player:
                #print("player found")
                amountInARow += 1
            else:
                amountInARow = 0

            i += 1
            j += 1
        #check outside of while loop
        if amountInARow == self.n:
            #print("Winner found in diagonal")
            return True
        #print("diag checked: " + str(diag))
        #print("in a row " + str(amountInARow))
        #get antidiagonal
        amountInARow = 0
        i = rowNum
        j = colNum 
        while i < self.rowCount - 1 and j > 0:
            i += 1
            j -= 1
        #trace along the antidiagonal
        #print("starting antidiag at " + str(i) + " " + str(j))
        antidiag = []
        while i >= 0 and j < self.columnCount:
            antidiag.append(self.board[i][j])
            if amountInARow == self.n:
                #print("Winner found in antidiagonal")
                return True
            if self.board[i][j] == self.player:
                amountInARow += 1
            else:
                amountInARow = 0
            i -= 1
            j += 1
        if amountInARow == self.n:
            #print("Winner found in antidiagonal")
            return True
        #print("antidiag checked: " + str(antidiag))
        return False
                


    #meant to be called immediately after dropping a piece
    #given an index, determines whether newly dropped piece in this location is a win
    #returns true false-- is game state a win?
    def isWin(self, row, column):
        #check horizontal
        if self._checkVertical(column) or self._checkHorizontal(row) or self._checkDiagonals(row, column):
            self.winningBoard = True
            #print("Win")
        else:
            self.winningBoard = False
        
        #use convolution operation for win detection
        
        
    #columns for player are numbered 0-(columnCount-1)
    #row index of where piece is placed
    def _drop_piece(self, colNumber):
        rowOut = 0
        for i in range(self.rowCount):
            if self.board[i][colNumber] != 0:
                rowOut = i-1
                self.board[i-1][colNumber] = self.player
                #if i == 1, that means the column is now full; remove from open columns
                if i == 1:
                    self.openColumns = self.openColumns[self.openColumns != colNumber]
                    #print(str(colNumber) + " removed from openColumns")
                    #print(self.openColumns)
                return rowOut
        #if all of them are 0, drop to bottom
        self.board[self.rowCount-1][colNumber] = self.player
        rowOut = self.rowCount - 1
        return rowOut

    #returns 1 for a player 1 win; 2 for a player 2 win; 3 for a draw; 0 for game in progress; -1 for invalid move
    def player_move(self, columnNumber):
        if columnNumber in self.openColumns:
            rowNumber = self._drop_piece(columnNumber)
            #print("Row piece dropped into: " + str(rowNumber))
            
            #increase numbed of moves executed
            self.movesExecuted += 1

            #update last move
            self.lastMove = (columnNumber, rowNumber)

            #check to see if it's a winner
            self.isWin(rowNumber, columnNumber)

            if self.winningBoard:
                return self.player
            self.swap_player()


            #if it's not a win, prepare for next round
            return 0

            
        else:
            #print("Column " + str(columnNumber) + " cannot be played")
            return -1 

    #returns boolean T/F whether board is a terminal state (win or draw)
    def terminal_test(self):
        #if it's a win or game board is full w/o win (draw)
        if self.winningBoard or np.count_nonzero(self.board) == self.board.size :
            return True
        
        else:
            return False

#returns a list of ConnectFourBoard objects representing next possible moves
def outputNextPossibleGameStates(board):
    #parameters for new board object
    openCols = board.get_openColumns()
    boardArray = board.get_board()
    player = board.get_player()
    colCount = board.get_columnCount()
    rowCount = board.get_rowCount()
    n = board.get_n()
    movesExecuted = board.get_movesExecuted()
    #stores tuples of (boardObj, intOfColPieceDroppedInto)
    output = []
    #print(openCols)
    for col in openCols:
        #make a deep copy of board array
        boardCopy = copy.deepcopy(boardArray)
        tempObj = ConnectFourBoard(colCount, rowCount, n, player, openCols, boardCopy, movesExecuted)
        tempObj.player_move(col)
        #print(tempObj)
        #print("WIN: ", str(tempObj.winningBoard))
        output.append((tempObj, col))

        #swap player


    #for board in output:
        #print(board[0].movesExecuted)
        #print(board)

    return output

#calculates numerical worth of terminal state
def _utility(gameState):
    #print("utility called")
    rows = gameState.get_rowCount()
    cols = gameState.get_columnCount()
    moves = gameState.get_movesExecuted()
    player = gameState.get_player()
    board = gameState.get_board()

    #first, determine if it's a tie
    if (np.count_nonzero(board) == board.size  and not gameState.winningBoard):
        #print("TIE")
        return 0
    elif gameState.winningBoard:
        #print("theres a winner")
        if player == 1.0: 
            #print("player one winner")
            return int(10000 * rows * cols / moves)
        elif player == 2.0:
            #print("player two winner")
            #print(int(-10000 * rows * cols / moves))
            return int(-10000 * rows * cols / moves)
    else:
        return 0


    