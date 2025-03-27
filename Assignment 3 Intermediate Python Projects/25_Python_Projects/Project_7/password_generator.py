import random
import string

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_special):
    # Available character pools
    upper = string.ascii_uppercase if use_uppercase else ""
    lower = string.ascii_lowercase if use_lowercase else ""
    digits = string.digits if use_numbers else ""
    special = string.punctuation if use_special else ""

    # Combine all selected character pools
    all_characters = upper + lower + digits + special

    if not all_characters:
        return "Error: No character types selected. Please try again!"

    # Ensure at least one character from each selected type
    password = []
    if use_uppercase:
        password.append(random.choice(upper))
    if use_lowercase:
        password.append(random.choice(lower))
    if use_numbers:
        password.append(random.choice(digits))
    if use_special:
        password.append(random.choice(special))

    # Fill the rest of the password
    remaining_length = length - len(password)
    if remaining_length > 0:
        password.extend(random.choices(all_characters, k=remaining_length))

    # Shuffle to prevent predictable patterns
    random.shuffle(password)

    return ''.join(password)

def main():
    print("Welcome to the Password Generator!")
    try:
        length = int(input("Enter the desired password length: "))
        use_uppercase = input("Include uppercase letters? (yes/no): ").lower() == "yes"
        use_lowercase = input("Include lowercase letters? (yes/no): ").lower() == "yes"
        use_numbers = input("Include numbers? (yes/no): ").lower() == "yes"
        use_special = input("Include special characters? (yes/no): ").lower() == "yes"

        if length < (use_uppercase + use_lowercase + use_numbers + use_special):
            print("Error: Password length is too short to include all selected character types!")
            return

        password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_special)
        print("\nGenerated Password:", password)
    except ValueError:
        print("Error: Please enter a valid number for the password length.")

if __name__ == "__main__":
    main()
