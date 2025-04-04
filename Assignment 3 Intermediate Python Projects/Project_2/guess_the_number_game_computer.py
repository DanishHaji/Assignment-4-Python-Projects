import random

def computer_guess():
    print("Think of a number between 1 and 100 and I will try to guess it.")
    print("Press 'Enter' when you are ready.")

    low = 1
    high = 100
    feedback = ''
    attempts = 0

    while feedback != 'c':
        if low > high:
            print("Hmm, something went wrong.")
            break

        guess = random.randint(low, high)
        attempts += 1
        print(f"My guess is {guess}.")
        feedback = input("Was my guess too high (H), too low (L), or correct (C)? ").lower()

        if feedback == 'h':
            high = guess - 1
        elif feedback == 'l':
            low = guess + 1
        elif feedback == 'c':
            print(f"Yay! I guessed your number {guess} in {attempts} attempts!")
        else:
            print("Please enter 'H', 'L', or 'C'.")
    
if __name__ == '__main__':
    computer_guess()