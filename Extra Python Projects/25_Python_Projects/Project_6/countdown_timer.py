import time
from colorama import Fore, Style, init
import os

# Initialize Colorama
init(autoreset=True)

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(Fore.CYAN + timer, end="\r") 
        time.sleep(1)
        seconds -= 1

    # Alert when timer ends
    print(Fore.RED + Style.BRIGHT + "Time is up!") 
    play_sound()

def play_sound():
    try:
        os.system('echo \a') 
    except Exception as e:
        print("Sound alert unavailable:", e)

if __name__ == "__main__":
    try:
        total_seconds = int(input(Fore.YELLOW + "Enter the countdown time in seconds: "))
        countdown_timer(total_seconds)
    except ValueError:
        print(Fore.RED + "Please enter a valid number!")
