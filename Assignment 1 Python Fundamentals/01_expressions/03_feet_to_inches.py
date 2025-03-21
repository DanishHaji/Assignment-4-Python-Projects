'''
Problem Statement
Converts feet to inches. Feet is an American unit of measurement. There are 12 inches per foot. Foot is the singular, and feet is the plural.
'''

INCHES_IN_FOOT: int = 12  # Conversion Factor (Constant Value)

def main():
    feet: float = float(input("Enter number of feet: "))
    inches: float = feet * INCHES_IN_FOOT
    print(str(feet) + " foot is equal to " + str(inches) + " inches.")

if __name__ == "__main__":
    main()
    