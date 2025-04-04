'''
Problem #1: List Practice
Now practice writing code with lists! Implement the functionality described in the comments below.

def main(): # Create a list called fruit_list that contains the following fruits: # 'apple', 'banana', 'orange', 'grape', 'pineapple'.
# Print the length of the list.
# Add 'mango' at the end of the list. 
# Print the updated list.
'''

def main():
    fruit_list: list = ['apple', 'banana', 'orange', 'grape', 'pineapple']
    print(fruit_list)

    lst_length: int = len(fruit_list)
    print(lst_length)

    fruit_list.append('mango')
    
    lst_length: int = len(fruit_list)
   
    print(fruit_list)
    print(lst_length)

if __name__ == "__main__":
    main()
