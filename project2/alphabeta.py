from connectfour import ConnectFourBoard
from connectfour import outputNextPossibleGameStates
from connectfour import _utility
from minimax import MinimaxInfo
import random
import time

#table to store minimax values
table = {}

def cutoff_test(depth, maxDepth):
    if depth == maxDepth:
        return True
    else:
        return False

#uses a heuristic to determine the numerical worth of a non-terminal state
def heuristic(state):
    #assign 10 points to n - 1 in a row
    #3 points to n-2 in a row
    #if there are two separate n-1 in a row add a bonus
    totalScore = 0
    pieceCoords = state.lastMove
    state.swap_player()

    if pieceCoords:
        colNum = pieceCoords[0]
        rowNum = pieceCoords[1]
        
        #check horizontal
        amountInARow = 0
        for loc in state.board[rowNum]:
            if loc == state.player:
                amountInARow += 1
                if amountInARow == state.n - 2:
                    totalScore += 3
                elif amountInARow == state.n - 1:
                    totalScore += 7
            else:
                amountInARow = 0
        
        #check vert
        amountInARow = 0
        for row in state.board:
            if row[colNum] == state.player:
                amountInARow += 1
                if amountInARow == state.n - 2:
                    totalScore += 3
                elif amountInARow == state.n - 1:
                    totalScore += 7 #only add 7 b/c prev iter. would've added 3
            else:
                amountInARow = 0
        amountInARow = 0
        
        i = rowNum
        j = colNum 
        while i > 0 and j > 0:
            i -= 1
            j -= 1

        #then we trace along the diagonal
        while i < state.rowCount and j < state.columnCount:
            if state.board[i][j] == state.player:
                amountInARow += 1
                if amountInARow == state.n - 2:
                    totalScore += 3
                elif amountInARow == state.n - 1:
                    totalScore += 7
            else:
                amountInARow = 0
            i += 1
            j += 1
        #check outside of while loop
        if amountInARow == state.n - 2 or amountInARow == state.n - 1:
            if amountInARow == state.n - 2:
                totalScore += 3
            else:
                totalScore += 10

        #get antidiagonal
        amountInARow = 0
        i = rowNum
        j = colNum 
        while i < state.rowCount - 1 and j > 0:
            i += 1
            j -= 1
        #trace along the antidiagonal
        while i >= 0 and j < state.columnCount:
            if state.board[i][j] == state.player:
                amountInARow += 1
                if amountInARow == state.n - 2:
                    totalScore += 3
                elif amountInARow == state.n - 1:
                    totalScore += 7
            else:
                amountInARow = 0
            i -= 1
            j += 1
        if amountInARow == state.n - 2 or amountInARow == state.n - 1:
            if amountInARow == state.n - 2:
                totalScore += 3
            else:
                totalScore += 10

        state.swap_player()
    

    totalScore = (-totalScore if state.player == 1.0 else totalScore)
    state.swap_player()


    return totalScore

def heuristic2(state):
    totalScore = 0

    playerToCheck = state.player

    boardArray = state.get_board()
    directions = [(0,1), (1,0), (1,-1), (1,1)]
    maxx = state.columnCount
    maxy = state.rowCount
    for d in directions:
        dx = d[0]
        dy = d[1]
        for x in range(maxx):
            for y in range(maxy):
                lastx = x + (state.n - 1)*dx
                lasty = y + (state.n - 1)*dy
                if (0 <= lastx and lastx < maxx and 0 <= lasty and lasty < maxy):
                    toCheck = []
                    for i in range(state.n):
                        moveX = i*dx
                        moveY = i*dy
                        #print(moveX)
                        #print(moveY)
                        toCheck.append(boardArray[y + moveY][x + moveX])
                    
                    amountInARow = 0
                    for elem in toCheck:
                        if elem == playerToCheck:
                            amountInARow += 1
                            if amountInARow == state.get_n() - 2:
                                totalScore += 3
                            elif amountInARow == state.get_n() - 1:
                                totalScore += 7
                        else:
                            amountInARow = 0
    
    return (-totalScore if playerToCheck == 2.0 else totalScore)


def _AlphaBeta_with_heuristics_recursive(gameState, alpha, beta, depth, maxDepth):
    alpha = alpha
    beta = beta
    
    if gameState in table.keys():
        return table[gameState].minimaxValue
    
    elif gameState.terminal_test():
        u = _utility(gameState)
        table[gameState] = MinimaxInfo(u, None)
        return u

    elif cutoff_test(depth, maxDepth):
        e = heuristic2(gameState)
        table[gameState] = MinimaxInfo(e, None)
        return e

    #game state with 1 as player means it's 1's turn to play next
    elif gameState.get_player() == 1: #MAX
        bestMinimaxSoFar = -float("inf")
        bestMoveForState = None
        for child in outputNextPossibleGameStates(gameState):
            childState = child[0]
            action = child[1] #column where piece is dropped 
            minimaxOfChild = _AlphaBeta_with_heuristics_recursive(childState, alpha, beta, depth+1, maxDepth)
            if minimaxOfChild > bestMinimaxSoFar:
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = action
            if bestMinimaxSoFar >= beta:
                return bestMinimaxSoFar
            alpha = max(alpha, bestMinimaxSoFar)
        table[gameState] = MinimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar

    elif gameState.get_player() == 2: #MIN
        bestMinimaxSoFar = float("inf")
        bestMoveForState = None 
        for child in outputNextPossibleGameStates(gameState):
            childState = child[0]
            action = child[1]
            minimaxOfChild = _AlphaBeta_with_heuristics_recursive(childState, alpha, beta, depth+1, maxDepth)
            if minimaxOfChild < bestMinimaxSoFar:
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = action
            if bestMinimaxSoFar <= alpha:
                return bestMinimaxSoFar
            beta = min(beta, bestMinimaxSoFar)
        table[gameState] = MinimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar


def AlphaBeta_w_heuristics(currentState, maxDepth):
    #reset transposition table
    table.clear()
    _AlphaBeta_with_heuristics_recursive(currentState, -float("inf"), float("inf"), 1, maxDepth)



def playWithAlphaBeta():
    rows = int(input("Enter rows: "))
    cols = int(input("Enter columns: "))
    n = int(input("Enter n-in-a-row: "))
    depth = int(input("Enter cutoff depth: "))

    userNum = int(input("User: do you want to play first (1) or second (2)? "))
    hintsOn = int(input("Do you want best move hints on? 1 for yes, 0 for no: ")) == 1
    cpuNum = userNum % 2 + 1.0

    print("Beginning game. ")

    winning = False 
    board = ConnectFourBoard(cols, rows, n)
    while not winning and not board.terminal_test():
        if board.get_player() == cpuNum:
            minOrMax = (" (MAX)" if cpuNum == 1.0 else " (MIN)")
            print("\nComputer's turn" + minOrMax)
            print(board)
    
            start_time = time.time()
            AlphaBeta_w_heuristics(board, depth)
            end_time = time.time()
            print("\nMinimax calculation completed in " + str(end_time - start_time))
            print("Transposition table has " + str(len(table)) + " states")
            print("The minimax value is: " + str(table[board].minimaxValue))
            print("Best column to pick is " + str(table[board].bestMoveForState))
            board.player_move(table[board].bestMoveForState)
            winning = board.winningBoard
            if winning:
                print(board)
                print("The computer wins!!")
        else:
            minOrMax = (" (MAX)" if userNum == 1.0 else " (MIN)")
            print("\nHuman's turn" + minOrMax)
            print(board)
            
            start_time = time.time()
            AlphaBeta_w_heuristics(board, depth)
            end_time = time.time()
            print("\nMinimax calculation completed in " + str(end_time - start_time))
            print("The minimax value is: " + str(table[board].minimaxValue))
            if hintsOn:
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
