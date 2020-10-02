from connectfour import ConnectFourBoard
import numpy as np
import copy

#returns a list of ConnectFourBoard objects representing next possible moves
def outputNextPossibleGameStates(board):
    #parameters for new board object
    openCols = board.get_openColumns()
    currBoard = board.get_board()
    colCount = board.get_columnCount()
    rowCount = board.get_rowCount()
    n = board.get_n()
    player = (2 if board.get_player() == 1 else 1)

    output = []

    for col in openCols:
        tempObj = copy.deepcopy(board)
        tempObj.player_move(openCols[col])
        output.append(tempObj)

    for board in output:
        print(board)




def main():
    gameBoard = ConnectFourBoard(7, 6, 4)
    print(gameBoard)

    col = int(input("Enter a column to drop piece: "))
    play = gameBoard.player_move(col)

    outputNextPossibleGameStates(gameBoard)


if __name__ == '__main__':
    main()