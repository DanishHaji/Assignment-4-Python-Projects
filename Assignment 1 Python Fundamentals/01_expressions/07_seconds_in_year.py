'''
Problem Statement
Use Python to calculate the number of seconds in a year, and tell the user what the result is in a nice print statement that looks like this (of course the value 5 should be the calculated number instead):

There are 5 seconds in a year!

You should use constants for this exercise -- there are 365 days in a year, 24 hours in a day, 60 minutes in an hour, and 60 seconds per minute.
'''

YEARS = 365
HOURS = 24
MINUTES = 60
SECONDS = 60

def main():
    seconds_in_year = YEARS * HOURS * MINUTES * SECONDS
    print(f"There are {seconds_in_year} seconds in a year!")

if __name__ == "__main__":
    main()
    