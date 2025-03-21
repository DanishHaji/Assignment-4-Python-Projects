'''
Problem Statement
Simulate rolling two dice, and prints results of each roll as well as the total.
'''

import random
SIDES = 6

def main():
    die1: int = random.randint(1, SIDES)
    die2: int = random.randint(1, SIDES)

    total: int = die1 + die2

    print("Dice have", SIDES, "sides each.")
    print("First die:", die1)
    print("Second die:", die2)
    print("Total of two dice:", total)
if __name__ =='__main__':
    main()
    


