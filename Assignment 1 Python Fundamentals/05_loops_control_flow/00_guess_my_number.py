'''
Problem Statement
Guess My Number

I am thinking of a number between 0 and 99... Enter a guess: 50 Your guess is too high

Enter a new number: 25 Your guess is too low

Enter a new number: 40 Your guess is too low

Enter a new number: 45 Your guess is too low

Enter a new number: 48 Congrats! The number was: 48
'''

import random

secret_number = random.randint(1, 99)

def main():
    while True:
        user_guess = int(input("Enter a number: "))
        if user_guess == secret_number:
            print(f"Congratulations! You have successfully guessed the secret number. {secret_number}")
        elif user_guess < secret_number:
            print("Your guess is too low")
        else:
            print("Your guess is too high")

if __name__ == '__main__':
    main()