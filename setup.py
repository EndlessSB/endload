import os
import bcrypt
import pyfiglet
from termcolor import colored

# Set console title
def set_console_title(title):
    if os.name == 'nt':  # Windows
        os.system(f'title {title}')
    else:
        print(f"\033]0;{title}\a", end='', flush=True)

# Print fancy ASCII text
def print_rainbow_text(text):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    ascii_art = pyfiglet.figlet_format(text)
    for i, line in enumerate(ascii_art.splitlines()):
        print(colored(line, colors[i % len(colors)]))

# Clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

set_console_title("Endload - Setup")
print_rainbow_text("Endload - Setup")

# Prompt user for credentials
username = input("Please set a username for the account: ").strip()
password = input("Please set a password for the account: ").strip()

password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")

try:
    with open(".env", "w", encoding="utf-8") as file:
        file.write(f"username={username}\n")
        file.write(f"password_hash={password_hash}\n")
    print("Success! - You can now run `main.py` safely!")
except Exception as e:
    print(f"An error occurred: {e}")
    exit()
