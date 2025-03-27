import time
import math

# Initialize the board
board = [" "] * 9

# Function banaya hai board show karnay k liye.
def display_board():
    print("\n")
    for i in range(3):
        print(" | ".join(board[i * 3: (i + 1) * 3]))
        if i < 2:
            print("-" * 9)
    print("\n")

# Function banaya hai winner check karnay k liye.
def check_winner(player):
    win_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)             # Diagonals
    ]
    
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == player:
            return True
    return False

# Function banaya hai board pora complete hogaya hai ya nhi. or draw to nhi hai
def is_draw():
    return " " not in board

# loop use kiya hai.
def play_game():
    current_player = "X"
    
    while True:
        display_board()
        try:
            move = int(input(f"Player {current_player}, enter your move (1-9): ")) - 1
            
            if move < 0 or move > 8 or board[move] != " ":
                print("Invalid move! Try again.")
                continue

            board[move] = current_player
            
            if check_winner(current_player):
                display_board()
                print(f"🎉 Player {current_player} wins! 🎉")
                break

            if is_draw():
                display_board()
                print("It's a draw! 🤝")
                break

            # player badlnay k liye
            current_player = "O" if current_player == "X" else "X"
            time.sleep(1)  # Small delay for better user experience
        
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 9.")

if __name__ == "__main__":
    print("🎮 Welcome to Tic-Tac-Toe CLI! 🎮")
    play_game()
