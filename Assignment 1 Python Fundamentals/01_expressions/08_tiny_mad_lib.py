'''
Problem Statement
Write a program which prompts the user for an adjective, then a noun, then a verb, and then prints a fun sentence with those words!

Mad Libs is a word game where players are prompted for one word at a time, and the words are eventually filled into the blanks of a word template to make an entertaining story! We've provided you with the beginning of a sentence (the SENTENCE_START constant) which will end in a user-inputted adjective, noun, and then verb.

Here's a sample run (user input is in bold italics):

Please type an adjective and press enter. tiny
Please type a noun and press enter. plant
Please type a verb and press enter. fly
Code in Place is fun. I learned to program and used Python to make my tiny plant fly!
'''

def main():
    # Define the sentence start
    SENTENCE_START = "Programming is"

    # Prompt the user for an adjective
    adjective = input("Please type an adjective and press enter: ")
    
    # Prompt the user for a noun
    noun = input("Please type a noun and press enter: ")
    
    # Prompt the user for a verb
    verb = input("Please type a verb and press enter: ")
    
    # Print the fun sentence with the user-inputted words
    print(f"{SENTENCE_START} fun. I learned to program and used Python to make my {adjective} {noun} {verb}!")

# Run the main function
if __name__ == "__main__":
    main()