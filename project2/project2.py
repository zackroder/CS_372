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

    for col in openCols:
        tempObj = copy.deepcopy(board)
        tempObj.player_move(openCols[col])
        output.append((tempObj, col))

    for board in output:
        print(board.movesExecuted)
        print(board)


#miniMax table to store values
#keys are ConnectFourBoard objects; values are MM value and best column to play
table = {}

#calculates numerical worth of terminal state
def _utility(gameState):
    rows = gameState.get_rowCount()
    cols = gameState.get_columnCount()
    moves = gameState.get_movesExecuted()
    player = gameState.get_player()
    board = gameState.get_board()

    #first, determine if it's a tie
    if (np.count_nonzero(board) == board.size  and not gameState.isWin()):
        return 0
    else:
        if player == 1:
            return int(10000 * rows * cols / moves)
        elif player == 2:
            return int(-10000 * rows * cols / moves)
#returns next player given a gamestate
def nextPlayer(gameState):
    player = gameState.get_player()

    return (2 if player == 1 else 1)

#takes board object and does minimax
def _MiniMaxRecursive(gameState):
    if gameState in table.keys():
        return table[gameState].minimaxValue

    elif gameState.terminal_test():
        u = _utility(gameState)
        table[gameState] = MinimaxInfo(u, None) #none b/c terminal state doesn't have a best move
    
    elif nextPlayer(gameState) == 1: #MAX
        bestMinimaxSoFar = -math.inf
        bestMoveForState = None
        for child in outputNextPossibleGameStates(gameState):
            childState = child[0]
            action = child[1] #column where piece is dropped 
            minimaxOfChild = _MiniMaxRecursive(childState)
            if minimaxOfChild > bestMinimaxSoFar:
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = action
        table[gameState] = MinimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar
    
    elif nextPlayer(gameState) == 2: #MIN
        bestMinimaxSoFar = math.inf
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
    _MiniMaxRecursive(initialBoard)


def main():
    MiniMax(6, 7, 4)


if __name__ == '__main__':
    main()