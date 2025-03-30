def print_board(board):
    """Prints the Sudoku board in a readable format."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21) # Separator between 3x3 grids
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ") # separate columns
            print(board[i][j], end=" ")
        print()

def is_valid(board, row, col, num):
    """Checks if placing 'num' at board[row][col] is valid."""
    # Check the row
    if num in board[row]:
        return False
    
    # check the column
    if num in [board[i][col] for i in range(9)]:
        return False
    
    # Check 3x3 box
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
            
    return True

def solve_sudoku(board):
    """Solves the Sudoku puzzle using backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0: # Find empty spot
                for num in range(1, 10): # Try numbers 1-9
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board): # Recursively solve
                            return True
                        board[row][col] = 0
                return False # No valid number found, backtrack
    
    return True # Solved

# Example Sudoku puzzle (0 represents empty cells)
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

print("\nUnsolved Sudoku: ")
print_board(sudoku_board)

if solve_sudoku(sudoku_board):
    print("\nSolved Sudoku: ")
    print_board(sudoku_board)
else:
    print("\nNo solution exists!")
    


