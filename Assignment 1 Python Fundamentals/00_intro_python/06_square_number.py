"""
Problem Statement

Ask the user for a number and print its square (the product of the number times itself).
Here's a sample run of the program (user input is in bold italics):
Type a number to see its square: 4
4.0 squared is 16.0

"""

def main():

    # Ask user for any number:
    num : int = float(input("Please enter a number: "))

    # Calculate the square of the number:
    square = num * num

    print(f"{num} squared is {square}")

if __name__ == "__main__":
    main()
