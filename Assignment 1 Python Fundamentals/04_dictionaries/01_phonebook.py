'''
Problem Statement
In this program we show an example of using dictionaries to keep track of information in a phonebook.
'''

def read_phone_numbers():

    phonebook = {}

    while True:
        name = input('Name: ')
        if name == '':
            break
        number = input('Phone number: ')
        phonebook[name] = number

    return phonebook

def print_phonebook(phonebook):
    for name in phonebook:
        print(f'{name}: {phonebook[name]}')

def lookup_numbers(phonebook):
    name = input('Name: ')
    if name not in phonebook:
        print(f'No entry found for {name}')
    else:
        print(f'{name}: {phonebook[name]}')

def main():
    phonebook = read_phone_numbers()
    print_phonebook(phonebook)
    lookup_numbers(phonebook)
if __name__ == '__main__':
    main()

