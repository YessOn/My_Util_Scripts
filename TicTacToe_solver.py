# Tic Tac Toe Game Coded using Python
import random

board = [" " for i in range(10)]

def insert_letter(letter, pos):
	board[pos] = letter

def sapce_is_free(pos):
	return board[pos] == ' '

def print_board(board):
    # "board" is a list of 10 strings representing the board (ignore index 0)
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('―――――――――――')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('―――――――――――')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])

def is_winner(board, letter):
	return ((board[7] == letter and board[8] == letter and board[9] == letter) or # across the top
    (board[4] == letter and board[5] == letter and board[6] == letter) or # across the middle
    (board[1] == letter and board[2] == letter and board[3] == letter) or # across the bottom
    (board[7] == letter and board[4] == letter and board[1] == letter) or # down the left side
    (board[8] == letter and board[5] == letter and board[2] == letter) or # down the middle
    (board[9] == letter and board[6] == letter and board[3] == letter) or # down the right side
    (board[7] == letter and board[5] == letter and board[3] == letter) or # diagonal
    (board[9] == letter and board[5] == letter and board[1] == letter)) # diagonal

def player_move():
    run = True
    while run:  # Keep looping until we get a valid move
        move = input('Please select a position to place an \'X\' (1-9): ')
        try:
            move = int(move)
            if move > 0 and move < 10:  # makes sure we type in a number between 1-9
                if sapce_is_free(move):  # check if the move we choose is valid (no other letter is there already)
                    run = False
                    insert_letter('X', move)
                else:
                    print('This postion is already occupied!')
            else:
                print('Please type a number within the range!')
        except:
            print('Please type a number!')

def comp_move():
	possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0] # Create a list of possible moves
	move = 0

    # Check for possible winning move to take or to block opponents winning move
	for let in ['O','X']:
		for i in possibleMoves:
			boardCopy = board[:]
			boardCopy[i] = let
			if is_winner(boardCopy, let):
				move = i
				return move

    # Try to take one of the corners
	cornersOpen = []
	for i in possibleMoves:
		if i in [1,3,7,9]:
			cornersOpen.append(i)
		if len(cornersOpen) > 0:
			move = select_random(cornersOpen)
		return move

    # Try to take the center
	if 5 in possibleMoves:
		move = 5
		return move

    # Take any edge
	edgesOpen = []
	for i in possibleMoves:
		if i in [2,4,6,8]:
			edgesOpen.append(i)
	if len(edgesOpen) > 0:
		move = select_random(edgesOpen)

	return move

def select_random(li):
    ln = len(li)
    r = random.randrange(0, ln)
    return li[r]

def is_board_full(board):
	# Since we always have one blank element in board we must use > 1
    if board.count(' ') > 1:
        return False
    else:
        return True

def main():
    # Main game loop
    print('Welcome to Tic Tac Toe, to win complete a straight line of your letter (Diagonal, Horizontal, Vertical). The board has positions 1-9 starting at the top left.')
    print_board(board)

    while not(is_board_full(board)):
        if not(is_winner(board, 'O')):
            player_move()
            print_board(board)
        else:
            print('O\'s win this time...')
            break

        if not(is_winner(board, 'X')):
            move = comp_move()
            if move == 0:
                print('Game is a Tie! No more spaces left to move.')
            else:
                insert_letter('O', move)
                print('Computer placed an \'O\' in position', move, ':')
                print_board(board)
        else:
            print('X\'s win, good job!')
            break

    if is_board_full(board):
        print('Game is a tie! No more spaces left to move.')


while True:
    answer = input('Do you want to play again? (Y/N)')
    if answer.lower() == 'y' or answer.lower == 'yes':
        board = [' ' for x in range(10)]
        print('――――――――――――――――――――――――――――――――――――――――――――')
        main()
    else:
        break

