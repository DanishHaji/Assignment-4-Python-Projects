import random


def guess_user():
    print("Welcome to the Guess the Number Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("Try to guess the number in as few attempts as possible.")

    number = random.randint(1, 100)
    attempts = 0
    guess = 0


    while guess != number:
        try:
            guess = int(input("Enter your guess:"))
            attempts += 1
            if guess > number:
                print("Too high. Try again.")
            elif guess < number:
                print("Too low. Try again.")
            else:
                print(f"Congratulations! You guessed the number {number} in {attempts} attempts.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 100.")

if __name__ == "__main__":
    guess_user()