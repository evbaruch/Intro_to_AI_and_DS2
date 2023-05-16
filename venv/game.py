# evyatar baruch - 323916403
# sapir bashan - 214103368
import copy
import numpy as np
EMPTY, BLACK, WHITE = '.', '●', '○'
HUMAN, COMPUTER = '●', '○'

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)
VIC=10000000 #The value of a winning board (for max)
LOSS=-VIC #The value of a losing board (for max)
TIE=0 #The value of a tie

'''
The state of the game is represented by a list of 4 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
   the comp's cells = COMPUTER and the human's = HUMAN
1. The heuristic value of the state.
2. Who's turn is it: HUMAN or COMPUTER
3. flag to end game

'''
# we understood that the colors on the bourd don't neet to swich but the player who starts needs to always be black
# if we understood wrong and in case that the human starts the colors on the bored need to change this would be the code
#
#  if choice.lower() == "h":
#            HUMAN, COMPUTER = '●', '○'
#            s[2] = HUMAN
#            s[0][44], s[0][45] = BLACK ,WHITE
#            s[0][54], s[0][55] = WHITE, BLACK
#            break
#The user decides who plays first
def whoIsFirst(s):
    global HUMAN,COMPUTER
    print("Please indicate the initial player for this game.")
    # this is a loop that will run until the user enters a valid choice
    # the user can enter either 'h' for human or 'c' for computer
    # the user's choice should be stored in s[2]
    # if the user enters 'h' then HUMAN should be set to '●' and COMPUTER to '○'
    # if the user enters 'c' then HUMAN should be set to '○' and COMPUTER to '●'
    # if the user enters anything else then print "Invalid choice. Please enter 'h' for human or 'c' for computer."
    # and ask the user to enter again
    while True:
        choice = input("Human (h)\nComputer (c)\n")
        if choice.lower() == "h":
            HUMAN, COMPUTER = '●', '○'
            s[2] = HUMAN
            break
        elif choice.lower() == "c":
            HUMAN, COMPUTER = '○', '●'
            s[2] = COMPUTER
            break
        else:
            print("Invalid choice. Please enter 'h' for human or 'c' for computer.")
    return s

def isHumTurn(s):
#Returns True iff it the human's turn to play
    return s[2]==HUMAN

def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

#The HUMAN plays first (=BLACK)
def create():
    global HUMAN,COMPUTER
    board = [EMPTY] * 100
    for i in squares():
        board[i] = EMPTY
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    HUMAN, COMPUTER = '●', '○'
    return [board,0.00001, HUMAN,False]

def printState(s):
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(s[0][begin:end]))
    print(rep)

    if s[1] == VIC:
        print("Ha ha ha I won!")
    elif s[1] == LOSS:
        print("You did it!")
    elif s[1] == TIE:
        print("It's a TIE")

def inputMove(s):
# Reads, enforces legality and executes the user's move.

    flag=True
    while flag:
        printState(s)
        move=int(input("To make your move enter a two digits number, the first number is row and the second is column" "\n" \
        "For example: if you want to choose the first row and the third column enter 13" "\n"\
        "Enter your next move: "))
        if isLegal(move, s) ==False:
            print("Illegal move.")
        else:
            flag=False
            makeMove(move,s)

#Returns the heuristic value of s
def value(s):
    # this is the heuristic function
    # the function's goel is to calculate the heuristic value of the givin state for the computer.
    # so the computer can decide which move is the best for him.
    # it is a linear combination of the following features:
    # 1. The difference in the number of pieces of the two players.
    # 2. the difference in number of surrounded pieces for each player.
    # 3. The difference in the number of legal moves of the two players (mobility).
    # 4. The difference in the number of pieces in the center of the board.
    # 5. The difference in the number of pieces that are in the corners.
    # the reason we chose these features is because these features are the ones that will most likley to affect the game.
    # and deciding which move is the best for the computer and who has the best chances to win.
    # and returns the heuristic value of the givin state to the computer.
    # using a calculation using all the features above.
    #(we found the calculation and features in a paper about the game from harvard university so it is most likley to be correct)

    #1. Calculate the number of pieces of each player
    COMPUTER_value = s[0].count(COMPUTER)
    HUMAN_value = s[0].count(HUMAN)
    EMPTY_value = s[0][11:89].count(EMPTY)

    # Convert game board matrix to numpy array
    board = np.array(s[0])
    board = board.reshape((10, 10))

    #2. Calculate the number of surrounded pieces for each player.
    num_surrounded_pieces = 0
    for i in range(1, 9):
        for j in range(1, 9):
            if board[i][j] != EMPTY:
                submatrix = board[i - 1:i + 2, j - 1:j + 2]
                num_surrounded_pieces += (np.count_nonzero(submatrix == EMPTY) == 0)

    #3. Calculate the mobility.
    # The mobility is the number of legal moves for the player.
    legal_moves = legalMoves(s)
    num_legal_moves = len(legal_moves)
    num_opponent_legal_moves = len(legalMoves([s[0], 0, COMPUTER if isHumTurn(s) else HUMAN, False]))

    #4. Calculate the control of the center.
    submatrix = board[4:6, 4:6]
    control_of_center = np.count_nonzero(submatrix == COMPUTER)

    #5. Calculate the control of the corners.
    # The corners are the 4 corners of the board.
    corners = [11, 12, 13, 14, 15, 16, 17, 18, 21, 28, 31, 38,
               41, 48, 51, 58, 61, 68, 71, 78, 81, 88]
    control_of_corners = 0
    for corner in corners:
        control_of_corners += (s[0][corner] == COMPUTER) - (s[0][corner] == HUMAN)

    # Calculate the heuristic value.
    # The heuristic value is a linear combination of the features above.
    # The weights of the features were confirmed by the paper from harvard university.
    s[1] = ((COMPUTER_value - HUMAN_value) +
            EMPTY_value * 0.5 +
            num_surrounded_pieces * 20 +
            (num_legal_moves - num_opponent_legal_moves) * 5 +
            control_of_center * 5 +
            control_of_corners * 25)

    # Return the heuristic value
    return s[1]



def isFinished(s):
#Returns True if the game ended
    ### your code here ###
    # Returns True if the game ended
    # The game ends when there are no more legal moves for both players
    # or when the board is full.

    # Check if the game is over
    if s[3]:
        # Check who won
        s[1] = VIC if s[0].count(HUMAN) < s[0].count(COMPUTER) else TIE if s[0].count(HUMAN) == s[0].count(COMPUTER) else LOSS
        return True

    # check if the current player can make a move
    # if not, switch the turn to the other player
    # if the other player can't make a move either, the game is over
    # and we check who won
    if len(legalMoves(s)) > 0:
        return False

    # Switch the turn to the other player if they can make a move
    # If the other player can't make a move either, the game is over
    # and we check who won
    s[2] = HUMAN if s[2] == COMPUTER else COMPUTER
    if len(legalMoves(s)) > 0:
        return False

    # No moves left for either player
    return True

def isLegal(move, s):
    hasbracket = lambda direction: findBracket(move, s, direction)
    return s[0][move] == EMPTY and any(map(hasbracket, DIRECTIONS))

# get a list of legal moves for the player
def legalMoves(s):
    return [sq for sq in squares() if isLegal(sq, s)]

# Is there any legal move for this player
def anyLegalMove(s):
    isAny = any(isLegal(sq, s) for sq in squares())
    if (not(isAny)):
        s[3] = True
    return isAny

def makeFlips(move, s, direction):
    bracket = findBracket(move, s, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        s[0][square] = s[2]
        square += direction

def changePlayer(s):
    if s[2] == COMPUTER:
            s[2] = HUMAN
    else:
       s[2] = COMPUTER

def makeMove(move, s):
    s[0][move] = s[2]
    for d in DIRECTIONS:
        makeFlips(move, s, d)
    value(s)
    changePlayer(s)
    return s

def whoWin (s):
    computerScore=0
    humanScore=0
    for sq in squares():
        piece = s[0][sq]
        if piece == COMPUTER:
            computerScore += 1
        elif piece == HUMAN:
            humanScore += 1
    if (computerScore>humanScore):
        return VIC

    elif (computerScore<humanScore):
        return LOSS

    elif (computerScore==HUMAN):
        return TIE

    return 0.00001 #not 0 because TIE is 0


def isValid(move):
    return isinstance(move, int) and move in squares()

def findBracket(square, s, direction):
    bracket = square + direction
    if s[0][bracket] == s[2]:
        return None
    opp = BLACK if s[2] is WHITE else WHITE
    while s[0][bracket] == opp:
        bracket += direction
    return None if s[0][bracket] in (EMPTY) else bracket

def getNext(s):
# returns a list of the next states of s
    ns=[]
    for m in legalMoves(s):
        tmp=copy.deepcopy(s)
        makeMove(m,tmp)
        ns+=[tmp]
    return ns
