'''
Problem Statement
Write a function that takes a list of numbers and returns the sum of those numbers.
'''

def add_many_numbers(numbers)-> int:
    total_sum = 0
    for num in numbers:
        total_sum += num
    return total_sum

def main():

    numbers : list[int] = [1, 2, 3, 4, 5]
    sum_of_numbers : int = add_many_numbers(numbers)
    print(f"The sum of the numbers in the list is: {sum_of_numbers}")

if __name__ == "__main__":
    main()



    