import random

class Minesweeper:
    def __init__(self, size=5, mines=5):
        """Initialize the game board with given size and mines"""
        self.size = size
        self.mines = mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.mine_positions = set()  # Fixed naming
        self.revealed = set()
        self.generate_mines()

    def generate_mines(self):
        """Randomly place mines on the board"""
        while len(self.mine_positions) < self.mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            self.mine_positions.add((row, col))

    def count_adjacent_mines(self, row, col):
        """Count mines in adjacent cells"""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = sum((row + dr, col + dc) in self.mine_positions for dr, dc in directions)
        return count

    def reveal(self, row, col):
        """Recursively reveal cells"""
        if (row, col) in self.revealed or row < 0 or col < 0 or row >= self.size or col >= self.size:
            return
        self.revealed.add((row, col))

        if (row, col) in self.mine_positions:
            print("\n💥 BOOM! You hit a mine! Game Over 💥")
            self.display_board(True)
            exit()
        
        adjacent_mines = self.count_adjacent_mines(row, col)
        if self.board[row][col] == ' ':  # Prevent overwriting already revealed cells
            self.board[row][col] = str(adjacent_mines) if adjacent_mines > 0 else ' '

        if adjacent_mines == 0:
            # Recursively reveal surrounding cells
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                self.reveal(row + dr, col + dc)

    def display_board(self, show_mines=False):
        """Print the board in a readable format"""
        print("\n   " + "  ".join(str(i) for i in range(self.size)))
        print("  " + "---" * self.size)
        for i in range(self.size):  # Fixed indentation
            row_display = []
            for j in range(self.size):
                if show_mines and (i, j) in self.mine_positions:
                    row_display.append("💣")
                elif (i, j) in self.revealed:
                    row_display.append(self.board[i][j])
                else:
                    row_display.append("⬜")
            print(f"{i} | " + "  ".join(row_display))

    def check_win(self):
        """Check if all non-mine cells are revealed"""
        return len(self.revealed) == (self.size * self.size) - self.mines

    def play(self):
        """Main game loop"""
        while True:
            self.display_board()
            try:
                row, col = map(int, input("\nEnter row and column (e.g., 2 3): ").split())
                if row < 0 or col < 0 or row >= self.size or col >= self.size:
                    print("Invalid input! Enter numbers within the board range.")
                    continue
                self.reveal(row, col)
                if self.check_win():
                    self.display_board(True)
                    print("\n🎉 Congratulations! You cleared the minefield! 🎉")
                    break
            except ValueError:
                print("Invalid input! Enter two numbers separated by space.")

# 🚀 Start the game
if __name__ == "__main__":
    game = Minesweeper(size=5, mines=5)
    game.play()
