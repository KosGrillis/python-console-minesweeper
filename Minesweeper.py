'''
minesweeper.py
Author: Kos Grillis
Version 1.0.1

A simple text based minesweeper game that runs in the python console.

Revision history:
16 Oct 2014: initial version. Incomplete.
17 Oct 2014: replaced check_history with check_board_pos to make next_move
             cleaner. Removed the history set and add_to_history.
             Added create_board.
18 Oct 2014: added check_loss and generate_loss_board. Made some minor
             alterations to existing functions.
20 Oct 2014: added check_win and print_message. Made modifications to
             validate_move so that it now provides information about the
             error should it return false.
22 Oct 2014: added count_mines. Modified compute_next_state
2 Nov 2014: added clear_board.
3 Nov 2014: replaced clear_board with floodfill. Errors in count_mines seem
            to have emerged.
4 Nov 2014: Fixed bugs in floodfill. Added interpret_move to clean up existing
            code.
5 Nov 2014: Minor changes in existing code. Game is now fully working.
11 Nov 2014: Changed code to be compatible with Python 3.4

To do: refactoring 
'''

from time import sleep
from enum import Enum
import random
import sys

class MessageType(Enum):
    GAME_START             = 1
    WIN                    = 2
    LOSS                   = 3
    NEW_GAME               = 4
    INVALID_MOVE           = 5
    ROW_INDEX_OUT_OF_RANGE = 6
    COL_INDEX_OUT_OF_RANGE = 7
    GAME_CLOSE             = 8
    MOVE_ALREADY_MADE      = 9

#define global variables...
NUM_MINES = 96
NUM_ROWS = 18
NUM_COLS = 25
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P', \
            'Q','R','S','T','U','V','W','X','Y']
ROW_INDEX = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15' \
             ,'16','17','18']
POSSIBLE_MINE_NUMBERS = ['1','2','3','4','5','6','7','8']

#Initialises the front-end board that will be pretty printed by user_disp...
CURRENT_BOARD = [['O ' for item in range(NUM_COLS)] for item in range(NUM_ROWS)]

def count_mines(BOARD, row, col):
    '''
    Called by create_board to count the number of mines in the neighbouring
    cells of (row, col). 
    '''
    #First note that cells is always a slice of the squares immediately
    #surrounding row, col and the cell of row, col itself...
    
    #First four statements are for the corners of the board...
    if row == 0 and col == 0:
        cells = BOARD[row][0:2] + BOARD[row + 1][0:2]
        num_mines = cells.count('X')
        return num_mines
    elif row == 0 and col == 24:
        cells = BOARD[row][22:] + BOARD[row + 1][22:]
        num_mines = cells.count('X')
        return num_mines
    elif row == 17 and col == 0:
        cells = BOARD[row - 1][0:2] + BOARD[row][0:2]
        num_mines = cells.count('X')
        return num_mines
    elif row == 17 and col == 24:
        cells = BOARD[row - 1][22:] + BOARD[row][22:]
        num_mines = cells.count('X')
        return num_mines
    
    #This statement for the top row excluding corners...
    elif row == 0 and (col != 0 or col != 24):
        cells = BOARD[row][col - 1: col + 2] + BOARD[row + 1][col - 1: col + 2]
        num_mines = cells.count('X')
        return num_mines
    
    #This statement for the bottom row excluding corners...
    elif row == 17 and (col != 0 or col != 24):
        cells = BOARD[row - 1][col - 1: col + 2] + BOARD[row][col - 1: col + 2]
        num_mines = cells.count('X')
        return num_mines
    
    #This statement is for the leftmost column excluding corners...
    elif (row != 0 or row != 17) and col == 0:
        cells = BOARD[row - 1][0:2] + BOARD[row][0:2] + BOARD[row + 1][0:2]
        num_mines = cells.count('X')
        return num_mines
    
    #This statement is for the leftmost column excluding corners...
    elif (row != 0 or row != 17) and col == 24:
        cells = BOARD[row - 1][23:] + BOARD[row][23:] + BOARD[row + 1][23:]
        num_mines = cells.count('X')
        return num_mines
    
    #This statement is for any position not covered by the previous 8...
    else:
        cells = BOARD[row - 1][col - 1:col + 2] + BOARD[row][col - 1:col + 2] \
                + BOARD[row + 1][col - 1: col + 2]
        num_mines = cells.count('X')
        return num_mines

def create_board():
    '''
    Generates the back-end board. The back end board contains
    'O' for an empty cell and 'X' for a mine. It also contains numbers
    which represent the number of surrounding mines for each cell.

    An example back_end board:
    
     1X1  1XX1 1X2X11XX2   1X
     11222222212121113X2  122
       1XX1  1X1    1332112X1
    1122321  1221   2XX32X222
    2X3X2  1222X11223XXX3221X
    X34X2 12XX4211XX23432X111
    12X21 1X5XX2112212X322111
    232211125X6X311113X3X1 1X
    XX11X212XX4X3X11X21322 11
    X31113X33453322211 2X2   
    222234X22XXX11X11112X3121
    2X2XXX223XX421123X2123X3X
    X2224321X34X2  2XX412X4X3
    11  1X12334X3113XX4X335X2
        1222XX3X21X23X323XX32
         1X3323332111112X422X
      11113X2 1XX21    2X2 11
      1X1 2X2 123X1    111   
    '''
    #Creates the board without numbers...
    cells = ['O'] * NUM_ROWS * NUM_COLS
    cells[:NUM_MINES] = ['X'] * NUM_MINES
    random.shuffle(cells)
    board = [cells[i::NUM_ROWS] for i in range(NUM_ROWS)]

    #Iterates through the board and calls upon count_mines
    #to count surrounding mines of each location...
    for row in range(len(board)):
        for col in range(len(board[row])):
            count = str(count_mines(board, row, col))
            if board[row][col] == 'X':
                board[row][col] = 'X'
            elif count in POSSIBLE_MINE_NUMBERS:
                board[row][col] = count
            else:
                #Places an empty space if count equals zero...
                board[row][col] = ' '
                
    return board

#Call create_board to set BOARD as a global variable...
BOARD = create_board()

def first_move_hint():
    '''
    Called upon by start and play_again to hint the user on what their first
    move should be. The hint will be a randomly determined empty space (i.e,
    one that will activate the recursive case of floodfill).
    '''
    #Finds all the empty spaces...
    possible_moves = []
    for row in range(len(BOARD)):
        for col in range(len(BOARD[row])):
            if BOARD[row][col] == ' ':
                move = row, col
                possible_moves.append(move)
                
    move = random.choice(possible_moves)
    row = move[0]
    col = move[1]
    user_row = str(row + 1)
    user_col = ALPHABET[col]
    print('HINT: try ' + user_row + ',' + user_col)

def print_message(message_type):
    '''
    handles all the message printing for the game.

    message types as follows:

    1 - game start
    2 - win
    3 - loss
    4 - new game
    5 - invalid move
    6 - row index out of range
    7 - col index out of range
    8 - game close
    9 - move already made
    '''
    if message_type == MessageType.GAME_START:
        print('Welcome to Python Minesweeper!') ; sleep(1)
        print()
        print('The board will be initialized with size 25 x 18 and 96 mines...') ; sleep(2)
        print()
        print('Good luck!') ; sleep(1)
        print()
        print('Let\'s begin!') ; sleep(1)
        print()
    elif message_type == MessageType.WIN:
        print()
        print('Congradulations! You win!')
    elif message_type == MessageType.LOSS:
        print()
        print('You hit a mine!') ; sleep(0.5)
        print()
        print('You lose!') ; sleep(0.5)
    elif message_type == MessageType.NEW_GAME:
        print()
        print('Starting new game...') ; sleep(1)
        print()
        print('The board will be initialized with size 25 x 18 and 96 mines...') ; sleep(2)
    elif message_type == MessageType.INVALID_MOVE:
        print()
        print('Invalid move!') ; sleep(0.5)
        print()
        print('You must enter a move in the form \'row, col, [flag]\'')
        print()
        next_move()
    elif message_type == MessageType.ROW_INDEX_OUT_OF_RANGE:
        print()
        print('Invalid move!') ; sleep(0.5)
        print()
        print('Row index must be a number between 1 and 18.')
        print()
        next_move()
    elif message_type == MessageType.COL_INDEX_OUT_OF_RANGE:
        print()
        print('Invalid move!') ; sleep(0.5)
        print()
        print('Col index must be a letter between A and Y.')
        print()
        next_move()
    elif message_type == MessageType.GAME_CLOSE:
        print()
        print('Goodbye!') ; sleep(2)
        sys.exit()
    elif message_type == MessageType.MOVE_ALREADY_MADE:
        print()
        print('Invalid move!') ; sleep(1)
        print()
        print('Try choosing an available space...') ; sleep(1)
        print()
        next_move()
            
def play_again():
    '''
    Called upon by next_move when the user wins or loses. Prompts the user
    to start a new game or exit.
    '''
    user_input = input('Play again? Y/N:')
    if user_input.upper() == 'Y':
        #Resets the back-end board...
        global BOARD
        BOARD = create_board()

        #Resets the front-end board...
        for row_index in range(0, NUM_ROWS):
            for col_index in range(0, NUM_COLS):
                CURRENT_BOARD[row_index][col_index] = 'O '

        #Starts new game...
        print_message(MessageType.NEW_GAME)
        user_disp(CURRENT_BOARD)
        first_move_hint()
        next_move()
    elif user_input.upper() == 'N':
        print_message(MessageType.GAME_CLOSE)

def interpret_move(move):
    '''
    Handles move interpretation for the game. Returns a 3-tuple of move
    information. The first two items contain row and col, respectively.
    the third item will be a zero if the move does not contain 'flag', and
    1 otherwise.
    '''
    #Since the move will always be validated first, we can set these
    #statements to known lengths...
    if len(move) == 3:
        row = int(move[0]) - 1
        col = ALPHABET.index(move[2].upper())
        return row, col, 0
    elif len(move) == 4:
        row = int(move[0:2]) - 1
        col = ALPHABET.index(move[3].upper())
        return row, col, 0
    elif len(move) == 8:
        row = int(move[0]) - 1
        col = ALPHABET.index(move[2].upper())
        return row, col, 1
    elif len(move) == 9:
        row = int(move[0:2]) - 1
        col = ALPHABET.index(move[3].upper())
        return row, col, 1
        
def check_board_pos(move):
    '''
    Called by next_move to check if a user can make a move
    in their specified location.

    Will return False if the user can't make their specified move,
    and True otherwise.

    The only reason this function will return False is if there is
    an empty space or a number in the user specified location, or if
    there is a flag in the location and the user has not specified that
    they want to remove it.
    '''
    row = interpret_move(move)[0]
    col = interpret_move(move)[1]
    flag = interpret_move(move)[2]
    
    if flag == 0:
        if CURRENT_BOARD[row][col] == '  ' or CURRENT_BOARD[row][col][0] in \
           POSSIBLE_MINE_NUMBERS or CURRENT_BOARD[row][col] == 'P ':
            return False
        else:
            return True
    else:
        if CURRENT_BOARD[row][col] == '  ' or CURRENT_BOARD[row][col][0] in \
           POSSIBLE_MINE_NUMBERS:
            return False
        else:
            return True

def check_loss(move):
    '''
    Called by next_move to check if there is a mine in
    the position specified by the user.

    Will return True if there is a mine in the position
    specified by the user, and False otherwise.
    '''
    row = interpret_move(move)[0]
    col = interpret_move(move)[1]
    flag = interpret_move(move)[2]
    
    if flag == 0:
        if BOARD[row][col] == 'X':
            return True
        else:
            return False
    #If a user is flagging a location, they should never lose...
    else:
        return False

def generate_loss_board():
    '''
    Called by next_move if check_loss returns true.
    Inserts the mines into CURRENT_BOARD for printing.

    If a mine has been correctly flagged by the user,
    a small x is inserted to show a disarmed mine.

    Incorrect flags are left as is.
    '''
    for row in range(0, NUM_ROWS):
        for col in range(0, NUM_COLS):
            if BOARD[row][col] == 'X':
                if CURRENT_BOARD[row][col] == 'O ':
                    CURRENT_BOARD[row][col] = 'X '
                elif CURRENT_BOARD[row][col] == 'P ':
                    CURRENT_BOARD[row][col] = 'x '

def check_win():
    '''
    Called by compute_next_state to check if the user has won.

    A win occurs when the entire board is clear, and
    there is a flag in each mine position.

    Use of the and operator makes this function a
    simple one.
    '''
    cells = CURRENT_BOARD.count('O ')
    flags = CURRENT_BOARD.count('P ')
    
    if cells == 0 and flags == NUM_MINES:
        return True
    else:
        return False

def validate_move(move):
    '''
    Called by next_move to check if the user entered string
    is in the form of a valid move.

    Valid move forms are as follows:

    [row],[col] eg 1,a or 17,a
    [row],[col],[flag] eg 1,a,flag or 17,a,flag

    note that [col] can be in either lowercase or uppercase.
    Also note that the comma can be a space instead.

    Will return True if the move is valid.

    If the move is not valid, it will return a tuple in the form
    (False, <error type>) where <error_type> will either 5, 6, or 7,
    to be easily passed to print_message for output.

    It will return 'Exception' if the move contains
    some form of the word 'exit'.
    '''
    if len(move) == 3:
        if move[1] == ',' or move[1] == ' ':
            if move[0] in ROW_INDEX:
                if move[len(move) - 1].upper() in ALPHABET:
                    return True
                else:
                    return False, 7
            else:
                return False, 6
        else:
            return False, 5
        
    elif len(move) == 4:
        if move[2] == ',' or move[2] == ' ':
            if move[0:2] in ROW_INDEX:
                if move[len(move) - 1].upper() in ALPHABET:
                    return True
                else:
                    return False, 7
            else:
                return False, 6
        elif move.lower() == 'exit':
            return 'Exception'
        else:
            return False, 5
        
    elif len(move) == 8:
        if ((move[1] == ',' or move[1] == ' ') and (move[3] == ',' or move[3] \
                                                    == ' ')):
            if move[4:].lower() == 'flag':
                if move[0] in ROW_INDEX:
                    if move[2].upper() in ALPHABET:
                        return True
                    else:
                        return False, 7
                else:
                    return False, 6
            else:
                return False, 5
        else:
            return False, 5
        
    elif len(move) == 9:
        if ((move[2] == ',' or move[2] == ' ') and (move[4] == ',' or move[4] \
                                                    == ' ')):
            if move[5:].lower() == 'flag':
                if move[0:2] in ROW_INDEX:
                    if move[3].upper() in ALPHABET:
                        return True
                    else:
                        return False, 7
                else:
                    return False, 6
            else:
                return False, 5
        else:
            return False, 5
    else:
        return False, 5

def floodfill(row, col):
    '''
    Implementation of the widely known floodfill algorithm to clear the board.

    Called by compute_next_state.
    '''
    #Base case...
    if BOARD[row][col] in POSSIBLE_MINE_NUMBERS:
        CURRENT_BOARD[row][col] = BOARD[row][col] + ' '
    #Recursive case...
    else:
        if CURRENT_BOARD[row][col] == 'O ':
            CURRENT_BOARD[row][col] = '  '
            if row > 0:
                floodfill(row - 1, col)
            if row < len(BOARD) - 1:
                floodfill(row + 1, col)
            if col > 0:
                floodfill(row, col - 1)
            if col < len(BOARD[row]) - 1:
                floodfill(row, col + 1)
        #Ensures that the algorithm skips over any flags that might be in the
        #way...
        elif CURRENT_BOARD[row][col] == 'P ':
            CURRENT_BOARD[row][col] = 'P '
            if row > 0:
                floodfill(row - 1, col)
            if row < len(BOARD) - 1:
                floodfill(row + 1, col)
            if col > 0:
                floodfill(row, col - 1)
            if col < len(BOARD[row]) - 1:
                floodfill(row, col + 1)
                
def compute_next_state(move):
    '''
    Called by next_move to compute the next state of
    the front-end board.
    '''
    row = interpret_move(move)[0]
    col = interpret_move(move)[1]
    flag = interpret_move(move)[2]

    #If the user wants to flag...
    if flag == 1:
        #If there is no flag, add one...
        if CURRENT_BOARD[row][col] == 'O ':
                CURRENT_BOARD[row][col] = 'P '
                user_disp(CURRENT_BOARD)
                next_move()
        #If there is a flag, remove it...
        elif CURRENT_BOARD[row][col] == 'P ':
                CURRENT_BOARD[row][col] = 'O '
                user_disp(CURRENT_BOARD)
                next_move()
    else:
        floodfill(row, col)
        user_disp(CURRENT_BOARD)
        if check_win() == False:
             next_move()
        else:
            print_message(MessageType.WIN)
            play_again()
            
def next_move():
    '''
    Is first called by start and promps the user to enter
    their move, before passing the move to other previously
    defined functions for computation.

    This function only calls itself if an invalid move is made.
    Otherwise, it is called by compute_next_state.
    '''
    move = input('Enter your next move:')
    
    if validate_move(move) == True:
        if check_loss(move) == False:
            if check_board_pos(move) == False:
                print_message(MessageType.MOVE_ALREADY_MADE)
            else:
                compute_next_state(move)
        else:
            generate_loss_board()
            user_disp(CURRENT_BOARD)
            print_message(MessageType.LOSS)
            play_again()

    #If invalid move...
    elif validate_move(move)[0] == False:
        error_type = validate_move(move)[1]
        print_message(error_type)
        
    #If the user wants to exit...
    elif validate_move(move) == 'Exception':
        print_message(MessageType.GAME_CLOSE)

def user_disp(CURRENT_BOARD):
    '''
    Pretty prints the board for the user.
    '''
    row_number = 1
    print()
    print('    [A][B][C][D][E][F][G][H][I][J][K][L][M][N][O][P][Q][R][S][T][U][V][W][X][Y]')
    for row in CURRENT_BOARD:
        if row_number < 10:
            print(' [' + str(row_number) + ']' + ' ' + ' '.join(row))
            row_number += 1
        else:
            print('[' + str(row_number) + ']' + ' ' + ' '.join(row))
            row_number += 1
    print()

def start():
    '''
    Is called when the script is run. Sets the user
    up for a new game.
    '''
    print_message(MessageType.GAME_START)
    user_disp(CURRENT_BOARD)
    first_move_hint()
    next_move()

#Call start for a new game upon running the script...
start()
