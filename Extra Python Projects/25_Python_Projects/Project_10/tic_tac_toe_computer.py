import math
import time

board = [" "] * 9  # Create an empty board


# Function to print the board
def display_board():
    print("\n")
    for i in range(3):
        print(" | ".join(board[i * 3: (i + 1) * 3]))
        if i < 2:
            print("-" * 9)
    print("\n")


# Function to check if a player has won
def check_winner(player):
    win_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]

    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == player:
            return True  # Player has won
    return False


# Function to check if the board is full (Draw)
def is_draw():
    return " " not in board


# Minimax Algorithm for AI decision-making
def minimax(is_maximizing, ai_player, human_player):
    if check_winner(ai_player):  # AI wins
        return 1
    if check_winner(human_player):  # Player wins
        return -1
    if is_draw():  # Draw
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = ai_player
                score = minimax(False, ai_player, human_player)
                board[i] = " "  # Undo move
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = human_player
                score = minimax(True, ai_player, human_player)
                board[i] = " "  # Undo move
                best_score = min(score, best_score)
        return best_score


# Function to make the AI move
def ai_move(ai_player, human_player):
    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = ai_player
            score = minimax(False, ai_player, human_player)
            board[i] = " "  # Undo move
            if score > best_score:
                best_score = score
                best_move = i

    board[best_move] = ai_player  # AI makes its move


# Main function to run the game
def play_game():
        human_player = input("Do you want to be X or O? ").upper()
        while human_player not in ["X", "O"]:
            print("Invalid choice! Please select 'X' or 'O'.")
            human_player = input("Do you want to be X or O? ").upper()

        ai_player = "O" if human_player == "X" else "X"
        current_player = "X"

        while True:
            display_board()
            if current_player == human_player:
                try:
                    move = int(input(f"Player {human_player}, enter your move (1-9): ")) - 1
                    if move < 0 or move > 8 or board[move] != " ":
                        print("Invalid move. Try again.")
                        continue
                    board[move] = human_player
                except ValueError:
                    print("Invalid input! Enter a number between 1 and 9.")
                    continue
            else:
                print("AI is thinking...")
                time.sleep(1)
                ai_move(ai_player, human_player)

            if check_winner(current_player):
                display_board()
                print(f"🎉 {current_player} wins! 🎉")
                break

            if is_draw():
                display_board()
                print("It's a draw! 🤝")
                break

            current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play_game()
