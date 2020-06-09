# Grid of 6x6
# grid = ('......',
#         '..B...',
#         'W.B.W.',
#         '......',
#         'W...W.',
#         'WW..W.')
my_board = [['.', '.', '.', '.', '.', '.'],
			['.', '.', 'B', '.', '.', '.'],
			['W', '.', 'B', '.', 'W', '.'],
			['.', '.', '.', '.', '.', '.'],
			['W', '.', '.', '.', 'W', '.'],
			['W', 'W', '.', '.', 'W', '.']]

my_answer =[['W', 'B', 'W', 'W', 'B', 'B'],
			['B', 'B', 'W', 'B', 'W', 'W'],
			['B', 'W', 'B', 'W', 'W', 'B'],
			['W', 'B', 'W', 'B', 'B', 'W'],
			['B', 'W', 'B', 'W', 'B', 'W'],
			['W', 'W', 'B', 'B', 'W', 'B']]

list_grid =[['W', 'B', '.', '.', 'B', '.'],
			['.', 'B', '.', '.', '.', '.'],
			['.', '.', '.', 'W', '.', '.'],
			['.', 'B', '.', '.', 'B', '.'],
			['.', '.', 'B', '.', 'B', '.'],
			['W', '.', '.', '.', '.', '.']]

events = ["B", "W"]

def generate_list_grid(grid):
	for i in grid:
		list_grid.append([j for j in i])
# generate_list_grid(grid)

def v_list(board, col): return [i[col] for i in board]

def find_empty(board):
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == ".":
				return (i, j) # Coordinates: col, row
	return None

def validate(board, event, row, col):
	# No three consecutive squares, horizontally or vertically, are the same colour
	if (col >= 2 and (event == board[row][col-1] and event == board[row][col-2])) or \
	(row >= 2 and event == board[row-1][col] and event == board[row-2][col]):return False

	# Check each row and column contains the same number of black and white squares.
	if (col == 5 and (board[row].count("W") > 3 or board[row].count("B") > 3)) or \
	(row == 5 and v_list(board, col).count("W") > 3 and v_list(board, col).count("B") > 3):return False
	# Else All Rules Are Satisfied
	return True

def solve(board):
	# print_board(board)
	# print("↹"*6)
	# print(find_empty(list_grid))
	find = find_empty(board)
	if not find:
		return True
	else:
		row, col = find
	for e in events:
		if validate(board, e, row, col):
			board[row][col] = e
			if solve(board):
				return True
			board[row][col] = "."
	return False

def print_board(board):
	for i in range(len(board)):
		for j in range(len(board[0])):
			if j == 5:
				print(board[i][j])
			else:
				print(board[i][j], end=" ")

# print_board(list_grid)

# print("↹"*10)
solve(list_grid)
print("ALgorithm")
print_board(list_grid)

print("↹"*6)
print("Right Answer")
print_board(my_answer)
# if v_list(list_grid, 0) == v_list(my_answer, 0):
# 	print("All is True")
# else:
# 	print("Sorry")