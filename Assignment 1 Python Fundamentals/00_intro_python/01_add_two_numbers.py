'''
Problem Statement

Write a Python program that takes two integer inputs from the user and calculates their sum. The program should perform the following tasks:
1-Prompt the user to enter the first number.
2-Read the input and convert it to an integer.
3-Prompt the user to enter the second number.
4-Read the input and convert it to an integer.
5-Calculate the sum of the two numbers.
6-Print the total sum with an appropriate message.
The provided solution demonstrates a working implementation of this problem, where the main() function guides the user through the process of entering two numbers and displays their sum.
'''

# def main():

#     # Prompt the user to enter the first number:
#     num1 = int(input("Enter a first number: "))

#     # Prompt the user to enter the second the number:
#     num2 = int(input("Enter a second number: "))

#     # Calculate the sum of two numbers:
#     sum = num1 + num2

#     # Print the total sum:
#     print(f"The sum of num1 and num2 is: {sum}.")


# if __name__ == "__main__":
#     main()

def main():

    num1 : str = input("Enter First Number: ")
    num1 : int = int(num1)
    num2 : str = input("Enter Second Number: ")
    num2 : int = int(num2)
    sum : int = num1 + num2
    print(f"The sum of num1 and num2 is: {sum}.")

if __name__ == "__main__":
    main()
    