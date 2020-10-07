##main function for project 2
from minimax import playWithMinimax
from alphabeta import playWithAlphaBeta

def main():
    print("Welcome to CONNECT-N!\n")

    gameType = int(input("Enter 1 to play with pure Minimax, 2 to play with Alpha-Beta (w/ Heuristic), or 0 to quit: "))

    while gameType != 0:
        if gameType == 1:
            playWithMinimax()
        
        elif gameType == 2:
            playWithAlphaBeta()

        gameType = int(input("Enter 1 to play with pure Minimax, 2 to play with Alpha-Beta (w/ Heuristic), or 0 to quit: "))


if __name__ == '__main__':
    main()