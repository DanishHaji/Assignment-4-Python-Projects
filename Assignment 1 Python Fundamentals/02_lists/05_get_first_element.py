'''
Problem Statement
Fill out the function get_first_element(lst) which takes in a list lst as a parameter and prints the first element in the list. The list is guaranteed to be non-empty. We've written some code for you which prompts the user to input the list one element at a time.
'''

def get_first_element(lst):

    if lst:
        print("First element:", lst[0])
    else:
        print("List is empty. No first element.")

def get_last_element():
    lst = []
    while True:
        elem: str = input('Please enter an element of the list or press enter to stop. ')
        if elem == '':
            break
        lst.append(elem)
    return lst
    
def main():
    lst = get_last_element()
    get_first_element(lst)

if __name__ == '__main__':
    main()


