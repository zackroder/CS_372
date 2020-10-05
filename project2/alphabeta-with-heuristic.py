from connectfour import ConnectFourBoard
from connectfour import outputNextPossibleGameStates
from connectfour import _utility
from minimax import MinimaxInfo

#table to store minimax values
table = {}

def cutoff_test(state, depth):
    if state.get_movesExecuted() == depth:
        return True
    else:
        return False

#uses a heuristic to determine the numerical worth of a non-terminal state
def heuristic(state):
    #TODO write heuristic
    return 0

def AlphaBeta_with_heuristics(gameState, alpha, beta, depth):
    if gameState in table.keys():
        return table[gameState].minimaxValue
    
    elif gameState.terminal_test():
        u = _utility(gameState)
        table[gameState] = MinimaxInfo(u, None)
        return u

    elif cutoff_test(gameState, depth):
        e = heuristic(gameState)
        table[gameState] = MinimaxInfo(e, None)
        return e

    #game state with 1 as player means it's 1's turn to play
    elif gameState.get_player() == 1: #MAX
        bestMinimaxSoFar = -float("inf")
        bestMoveForState = None
        for child in outputNextPossibleGameStates(gameState):
            childState = child[0]
            action = child[1] #column where piece is dropped 
            minimaxOfChild = AlphaBeta_with_heuristics(childState, alpha, beta, depth+1)
            if minimaxOfChild > bestMinimaxSoFar:
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = action
            if minimaxSoFar >= beta:
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
            minimaxOfChild = AlphaBeta_with_heuristics(childState, alpha, beta, depth+1)
            if minimaxOfChild < bestMinimaxSoFar:
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = a
            if minimaxSoFar <= alpha:
                return bestMinimaxSoFar
            beta = min(beta, bestMinimaxSoFar)
        table[gameState] = MinimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar