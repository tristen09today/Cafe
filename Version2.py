# Version 2 of the app should be more complex involving Easy GUI 
# Year eligibility for the app is 9-13
from easygui import *
import os
import csv

# Constants
YEAR_ELIGIBILITY = [9, 10, 11, 12, 13]
MAX_QUANTITY = 50
MIN_QUANTITY = 1
MENU_FILE  = "menu.txt"
LOGIN_FILE = "Login.txt"

# Ensure login file exists
if not os.path.exists(LOGIN_FILE):
    open(LOGIN_FILE, "w").close()

# Load users from file
def load_users():
    users = {}
    with open(LOGIN_FILE, "r") as file:
        for line in file:
            if line.strip():
                username, password = line.strip().split(",")
                users[username] = password
    return users

# Save new user to file
def save_user(username, password):
    with open(LOGIN_FILE, "a") as file:
        file.write(f"{username},{password}\n")

# Helper for non-empty input
def get_non_empty_input(prompt, is_password=False):
    while True:
        value = passwordbox(prompt) if is_password else enterbox(prompt)
        if value:
            return value
        msgbox("Input cannot be empty. Please try again.")

# Login or signup interface (improved version)
def login_system():
    users = load_users()

    while True:
        action = buttonbox("Welcome to the Café App!\nDo you want to Log In or Sign Up?", "Login System", choices=["Log In", "Sign Up", "Exit"])

        if action == "Exit":
            msgbox("Exiting app. Goodbye!", "Exit")
            exit()

        elif action == "Sign Up":
            while True:
                username = get_non_empty_input("Create a new username:")
                if username in users:
                    msgbox("That username already exists. Try a different one.")
                    continue

                password = get_non_empty_input("Create a password:", is_password=True)
                confirm = get_non_empty_input("Confirm your password:", is_password=True)

                if password != confirm:
                    msgbox("Passwords do not match. Try again.")
                    continue

                save_user(username, password)
                users[username] = password
                msgbox("Account created successfully!")
                break

        elif action == "Log In":
            for attempt in range(3):
                username = get_non_empty_input("Enter your username:")
                password = get_non_empty_input("Enter your password:", is_password=True)

                if users.get(username) == password:
                    msgbox(f"Welcome, {username}!")
                    return  # Exit on success

                msgbox("Incorrect username or password.")
            msgbox("Too many failed attempts. Exiting.")
            exit()

# Load menu items
def load_menu():
    menu_items = {}
    with open(MENU_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            number, name, price = row
            menu_items[int(number)] = {"name": name.strip(), "price": float(price.strip())}
    return menu_items

# Quantity validation
def is_valid_quantity(qty):
    return MIN_QUANTITY <= qty <= MAX_QUANTITY

# Year level validation
def get_year_level():
    while True:
        year_str = enterbox("Enter your year level: (9-13)")
        if year_str is None:
            msgbox("Exiting app.")
            exit()
        try:
            year = int(year_str)
            if year in YEAR_ELIGIBILITY:
                msgbox("Welcome to the Café App!")
                return year
            else:
                msgbox("You are not eligible to use the app!")
                exit()
        except ValueError:
            msgbox("Please enter a valid number.")

# Display menu
def display_menu(menu_items):
    menu_text = "Café Menu:\n"
    for number in sorted(menu_items):
        item = menu_items[number]
        menu_text += f"{number}. {item['name']} - ${item['price']:.2f}\n"
    textbox("Menu", "Available Items", menu_text)

# Take order
def get_order(menu_items):
    cart = {}
    item_choices = [f"{num}. {item['name']}" for num, item in menu_items.items()]
    item_choices.append("Finish Order")

    while True:
        choice_str = buttonbox("Select an item to order:", "Make Your Order", item_choices)
        if choice_str == "Finish Order":
            break
        item_number = int(choice_str.split(".")[0])
        qty_str = enterbox(f"Enter quantity for {menu_items[item_number]['name']} (1-50):")
        if qty_str is None:
            continue
        try:
            qty = int(qty_str)
            if is_valid_quantity(qty):
                cart[item_number] = cart.get(item_number, 0) + qty
                msgbox(f"Added {qty} of {menu_items[item_number]['name']} to your order.")
            else:
                msgbox(f"Quantity must be between {MIN_QUANTITY} and {MAX_QUANTITY}.")
        except ValueError:
            msgbox("Please enter a valid number.")
    return cart

# Display order summary
def display_summary(cart, menu_items):
    if not cart:
        msgbox("You have not ordered anything.")
        return
    summary = "Order Summary:\n"
    total = 0
    for number, quantity in cart.items():
        item = menu_items[number]
        cost = item["price"] * quantity
        summary += f"{item['name']} x{quantity} = ${cost:.2f}\n"
        total += cost
    summary += f"\nTotal Price: ${total:.2f}"
    textbox("Order Summary", "Your Order", summary)

# Run the program
def main():
    login_system()
    get_year_level()
    menu_items = load_menu()
    display_menu(menu_items)
    cart = get_order(menu_items)
    display_summary(cart, menu_items)

main()
