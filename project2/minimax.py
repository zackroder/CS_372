from connectfour import ConnectFourBoard
from connectfour import outputNextPossibleGameStates
from connectfour import _utility
import numpy as np
import math
from dataclasses import dataclass
import sys
import time
import cProfile

@dataclass
class MinimaxInfo:
    minimaxValue: int
    bestMoveForState: int 



#returns next player given a gamestate
def nextPlayer(gameState):
    return gameState.get_player()
    #the notion of "next player" under my connect 4 board object is confusing
    #player corresponds to the player who receives the board in its current state
    #return (2.0 if player == 1.0 else 1.0)

#miniMax table to store values
#keys are ConnectFourBoard objects; values are MM value and best column to play
table = {}
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
    print("Size of transposition table: " + str(len(table)))


def playWithMinimax():
    rows = int(input("Enter rows: "))
    cols = int(input("Enter columns: "))
    n = int(input("Enter n-in-a-row: "))

    start_time = time.time()
    MiniMax(rows,cols,n)
    end_time = time.time()
    print("Total time to solve game tree: " + str(end_time-start_time))
    userNum = int(input("User: do you want to play first (1) or second (2)? "))
    cpuNum = userNum % 2 + 1.0

    print("Beginning game. ")

    winning = False 
    board = ConnectFourBoard(cols, rows, n)
    while not winning and not board.terminal_test():
        if board.get_player() == cpuNum:
            print("\nComputer's turn")
            print(board)
            print("The best minimax value is: " + str(table[board].minimaxValue))
            print("Best column to pick is " + str(table[board].bestMoveForState))
            board.player_move(table[board].bestMoveForState)
            winning = board.winningBoard
            if winning:
                print(board)
                print("CPU wins!")
        else:
            print("\nHumans's turn")
            print(board)
            print("The best minimax value is: " + str(table[board].minimaxValue))
            print("Best column to pick is " + str(table[board].bestMoveForState))
            col = int(input("pick a column: "))
            board.player_move(col)
            winning = board.winningBoard
            if winning:
                print(board)
                print("Player wins!")
    
    if not winning and board.terminal_test():
        print('\n')
        print(board)
        print("Tie!")
    
    table.clear()
        