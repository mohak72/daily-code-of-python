"""
Password Generator
Generate secure random passwords with customizable options
"""

import random
import string
from typing import List


def generate_password(length: int = 12, use_uppercase: bool = True,
                     use_lowercase: bool = True, use_digits: bool = True,
                     use_special: bool = True) -> str:
    """Generate a random password based on specified criteria"""

    if length < 4:
        raise ValueError("Password length must be at least 4 characters")

    char_pool = ""
    required_chars = []

    if use_lowercase:
        char_pool += string.ascii_lowercase
        required_chars.append(random.choice(string.ascii_lowercase))

    if use_uppercase:
        char_pool += string.ascii_uppercase
        required_chars.append(random.choice(string.ascii_uppercase))

    if use_digits:
        char_pool += string.digits
        required_chars.append(random.choice(string.digits))

    if use_special:
        char_pool += string.punctuation
        required_chars.append(random.choice(string.punctuation))

    if not char_pool:
        raise ValueError("At least one character type must be selected")

    # Fill remaining length with random characters
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [random.choice(char_pool) for _ in range(remaining_length)]

    # Shuffle to avoid predictable patterns
    random.shuffle(password_chars)

    return ''.join(password_chars)


def calculate_password_strength(password: str) -> tuple:
    """Calculate password strength (score out of 5, description)"""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    if any(c.islower() for c in password):
        score += 0.5
    if any(c.isupper() for c in password):
        score += 0.5
    if any(c.isdigit() for c in password):
        score += 0.5
    if any(c in string.punctuation for c in password):
        score += 0.5

    score = int(score)

    if score <= 1:
        strength = "Very Weak"
    elif score == 2:
        strength = "Weak"
    elif score == 3:
        strength = "Medium"
    elif score == 4:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return score, strength


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Get yes/no input from user"""
    default_str = "Y/n" if default else "y/N"
    while True:
        choice = input(f"{prompt} ({default_str}): ").strip().lower()
        if choice == '':
            return default
        if choice in ['y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")


def main():
    """Main program loop"""
    print("\n" + "="*50)
    print("  PASSWORD GENERATOR")
    print("="*50)

    while True:
        print("\nPassword Options:")

        # Get password length
        while True:
            try:
                length = input("Password length (default 12): ").strip()
                length = int(length) if length else 12
                if length < 4:
                    print("Password must be at least 4 characters long!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number!")

        # Get character type preferences
        use_uppercase = get_yes_no("Include uppercase letters?", True)
        use_lowercase = get_yes_no("Include lowercase letters?", True)
        use_digits = get_yes_no("Include digits?", True)
        use_special = get_yes_no("Include special characters?", True)

        # Get number of passwords
        while True:
            try:
                count = input("\nHow many passwords to generate (default 1): ").strip()
                count = int(count) if count else 1
                if count < 1:
                    print("Please enter a positive number!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number!")

        # Generate passwords
        print("\n" + "-"*50)
        print("Generated Passwords:")
        print("-"*50)

        try:
            for i in range(count):
                password = generate_password(
                    length, use_uppercase, use_lowercase,
                    use_digits, use_special
                )
                score, strength = calculate_password_strength(password)
                print(f"{i+1}. {password}")
                print(f"   Strength: [{score}/5] {strength}")
                print()
        except ValueError as e:
            print(f"\nError: {e}")

        # Ask to generate more
        if not get_yes_no("\nGenerate more passwords?", False):
            break

    print("\nThank you for using Password Generator!\n")


if __name__ == "__main__":
    main()
