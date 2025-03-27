import random

word_list = ['python', 'hangman', 'program', 'computer', 'science', 'mathematics', 'player', 'condition', 'reverse', 'water', 'board', 'geeks']

def play_hangman():
    word = random.choice(word_list)
    guessed_word = ["_"] * len(word)
    attempts = 6
    guessed_letters = set()
    hints_used = False 

    print("\n🎉 Let's play Hangman! 🎉")
    print("Guess the word:")
    print(" ".join(guessed_word))

    while attempts > 0 and "_" in guessed_word:
        print(f"\nGuessed letters: {', '.join(guessed_letters) if guessed_letters else 'None'}")
        guess = input("Enter a letter (or type 'hint' for help): ").lower().strip()

        # Handle hint option
        if guess == "hint" and not hints_used:
            hints_used = True
            for i, letter in enumerate(word):
                if guessed_word[i] == "_":
                    guessed_word[i] = letter
                    print(f"💡 Hint used! A letter is revealed: {' '.join(guessed_word)}")
                    break
            continue
        elif guess == "hint":
            print("⚠️ You have already used your hint!")
            continue

        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("❌ Invalid input. Please enter a single letter.")
            continue
        if guess in guessed_letters:
            print(f"⚠️ You already guessed '{guess}'. Try a different letter.")
            continue

        # Store guessed letter
        guessed_letters.add(guess)

        # Check if the letter is in the word
        if guess in word:
            print(f"✅ Good job! '{guess}' is in the word.")
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed_word[i] = guess
        else:
            attempts -= 1
            print(f"❌ Sorry, '{guess}' is not in the word.")
            print(f"🔥 Attempts left: {attempts}")

        print(" ".join(guessed_word))

    # Final game result
    if "_" not in guessed_word:
        print("\n🎉 Congratulations! You guessed the word:", word)
    else:
        print("\n💀 Game over! The word was:", word)

def main():
    while True:
        play_hangman()
        replay = input("\n🔄 Do you want to play again? (yes/no): ").lower().strip()
        if replay != "yes":
            print("👋 Thanks for playing! See you next time.")
            break

if __name__ == "__main__":
    main()
