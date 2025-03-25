'''
Problem Statement
Fill out the function count_even(lst) which

first populates a list by prompting the user for integers until they press enter (please use the prompt "Enter an integer or press enter to stop: "),

and then prints the number of even numbers in the list.

If you'd prefer to focus on the second task only, scroll down for our implementation of the first task!
'''

def count_even(lst):
    count = 0
    for i in lst:
        if i % 2 == 0:
            count += 1
    print(count)

def get_lst_of_ints():
    lst = []
    user_input = input("Enter an integer or press enter to stop: ")
    while user_input != "":
        lst.append(int(user_input))
        user_input = input("Enter an integer or press enter to stop: ")
    return lst

def main():
    lst = get_lst_of_ints()
    count_even(lst)

if __name__ == '__main__':
    main()
