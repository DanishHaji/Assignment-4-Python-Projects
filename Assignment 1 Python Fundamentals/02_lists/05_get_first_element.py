'''
Problem Statement
Fill out the function get_first_element(lst) which takes in a list lst as a parameter and prints the first element in the list. The list is guaranteed to be non-empty. We've written some code for you which prompts the user to input the list one element at a time.
'''

def get_first_element(lst):

    print(lst[0])

def get_last_element():
    lst = []
    elem: str = input('Please enter an element of the list or press enter to stop. ')
    while elem != '':
        lst.append(elem)
        elem = input('Please enter an element of the list or press enter to stop. ')
        return elem
    
def main():
    lst = get_last_element()
    get_first_element(lst)

if __name__ == '__main__':
    main()


