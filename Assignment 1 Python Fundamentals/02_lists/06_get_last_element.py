'''
Problem Statement
Fill out the function get_last_element(lst) which takes in a list lst as a parameter and prints the last element in the list. The list is guaranteed to be non-empty, but there are no guarantees on its length.
'''

def get_last_element(lst):
    """Prints the last element of a non-empty list."""
    print(lst[-1])  # Access the last element directly

def get_lst():
    """Takes user input to create a list until an empty input is provided."""
    lst = []
    while True:
        elem = input('Please enter an element of the list or press enter to stop: ')
        if elem == '':
            break  # Stop when the user presses enter
        lst.append(elem)  # Store input as a string

    return lst  # Return the full list

def main():
    """Gets the list from the user and prints the last element."""
    lst = get_lst()  # Get user input list
    if lst:  # Ensure the list is not empty before calling the function
        get_last_element(lst)

if __name__ == '__main__':
    main()

