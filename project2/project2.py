from connectfour import ConnectFourBoard
import numpy as np
import copy
import math
from dataclasses import dataclass

@dataclass
class MinimaxInfo:
    minimaxValue: int
    bestMoveForState: int 


#returns a list of ConnectFourBoard objects representing next possible moves
def outputNextPossibleGameStates(board):
    #parameters for new board object
    openCols = board.get_openColumns()
    currBoard = board.get_board()
    colCount = board.get_columnCount()
    rowCount = board.get_rowCount()
    n = board.get_n()
    player = (2 if board.get_player() == 1 else 1)

    #stores tuples of (boardObj, intOfColPieceDroppedInto)
    output = []
    #print(openCols)
    for col in openCols:
        tempObj = copy.deepcopy(board)
        tempObj.swap_player()
        tempObj.player_move(col)
        #print(tempObj)
        #print("WIN: ", str(tempObj.winningBoard))
        output.append((tempObj, col))

    #for board in output:
        #print(board[0].movesExecuted)
        #print(board)

    return output


#miniMax table to store values
#keys are ConnectFourBoard objects; values are MM value and best column to play
table = {}

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
#returns next player given a gamestate
def nextPlayer(gameState):
    player = gameState.get_player()

    return (2.0 if player == 1.0 else 1.0)

#takes board object and does minimax
def _MiniMaxRecursive(gameState):
    if gameState in table.keys():
        return table[gameState].minimaxValue

    elif gameState.terminal_test():
        u = _utility(gameState)
        table[gameState] = MinimaxInfo(u, None) #none b/c terminal state doesn't have a best move
        return u

    elif nextPlayer(gameState) == 1: #MAX
        bestMinimaxSoFar = -float("inf")
        bestMoveForState = None
        for child in outputNextPossibleGameStates(gameState):
            childState = child[0]
            action = child[1] #column where piece is dropped 
            minimaxOfChild = _MiniMaxRecursive(childState)
            #print(bestMinimaxSoFar)
            if minimaxOfChild > bestMinimaxSoFar:
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = action
        table[gameState] = MinimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar
    
    elif nextPlayer(gameState) == 2: #MIN
        bestMinimaxSoFar = float("inf")
        bestMoveForState = None
        for child in outputNextPossibleGameStates(gameState):
            childState = child[0]
            action = child[1]
            minimaxOfChild = _MiniMaxRecursive(childState)
            if minimaxOfChild < bestMinimaxSoFar:
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = action
        table[gameState] = MinimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar
    


#returns a transposition table with best moves for any given gamestate
def MiniMax(rows, columns, n):
    initialBoard = ConnectFourBoard(columns, rows, n)
    #print(initialBoard.n)
    _MiniMaxRecursive(initialBoard)


def main():
    print(MiniMax(4, 5, 3))
    print("Size of transposition table: " + str(len(table)))
    board1 = ConnectFourBoard(5, 4, 3)
    board2 = ConnectFourBoard(5,4,3)
    print(table[board1].minimaxValue)

if __name__ == '__main__':
    main()