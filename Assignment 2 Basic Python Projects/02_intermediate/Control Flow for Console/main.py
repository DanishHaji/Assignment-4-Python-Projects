'''
Problem: High Low
We want you to gain more experience working with control flow and Booleans in Python. To do this, we are going to have you develop a game! The game is called High-Low and the way it's played goes as follows:
Two numbers are generated from 1 to 100 (inclusive on both ends): one for you and one for a computer, who will be your opponent. You can see your number, but not the computer's!
You make a guess, saying your number is either higher than or lower than the computer's number
If your guess matches the truth (ex. you guess your number is higher, and then your number is actually higher than the computer's), you get a point!
These steps make up one round of the game. The game is over after all rounds have been played.
We've provided a sample run below.
'''

import random

NUM_ROUNDS = 5

def main():
    print("Welcome to the High-Low game!")
    print("You will play against the computer.")

    your_score = 0
    computer_score = 0

    for i in range(NUM_ROUNDS):
        print(f"\nRound {i + 1} of {NUM_ROUNDS}")
        your_number = random.randint(1, 100)
        computer_number = random.randint(1, 100)
        print(f"Your number is: {your_number}")

        choice: str = input("Do you think your number is higher or lower than the computer's number? (h/l): ").strip().lower()

        higher_and_correct: bool = choice == "h" and your_number > computer_number
        lower_and_correct: bool = choice == "l" and your_number < computer_number

        if higher_and_correct or lower_and_correct:
            print("Correct! You get a point.")
            your_score += 1
        else:
            print("Incorrect! The computer gets a point.")
            computer_score += 1
        
        print("Your score is now", your_score)
        print()

        print("Thanks for playing")

if __name__ == "__main__":
    main()
    

