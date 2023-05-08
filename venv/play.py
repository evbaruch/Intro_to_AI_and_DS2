import alphaBetaPrunning
import game

board = game.create()
# call the function to decide who is first
game.whoIsFirst(board)

while game.anyLegalMove(board):
    if game.isHumTurn(board):
        game.inputMove(board)
    else:
        board = alphaBetaPrunning.go(board)

    if (not game.anyLegalMove(board)):
        print("Player ", board[2], " :")
        game.changePlayer(board)
        print("You have no more moves", "\n", "Change player to ", board[2], "\n")

game.isFinished(board)
game.printState(board)
