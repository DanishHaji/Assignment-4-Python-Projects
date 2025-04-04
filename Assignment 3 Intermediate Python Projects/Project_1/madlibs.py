def madlibs_game():
    # Ask the user for a series of words to fill the blanks:
    noun : str = input("Enter a noun: ")
    verb : str = input("Enter a verb: ")
    adjective : str = input("Enter an adjective: ")
    place : str = input("Enter a place: ")

    # Display the story with the blanks filled in:
    story = f"Take your {adjective} {noun} and {verb} it at the {place}!"


    print("\nHere's your MAd libs story:")
    print(story)

if __name__ == "__main__":
    madlibs_game()
