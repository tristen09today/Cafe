# Version 2 of the app should be more complex involving Easy GUI 
from easygui import *
import csv

# Constants
YEAR_ELIGIBILITY = [9, 10, 11, 12, 13]
MAX_QUANTITY = 50
MIN_QUANTITY = 1
MENU_FILE  = "menu.txt"
# Login system constants
LOGIN_FILE = "Login.txt"
LOGIN_ATTEMPS = 3   
MIN_PASS_LENGTH = 4
MAX_PASS_LENGTH = 15
MIN_USER_LENGTH = 3
MAX_USER_LENGTH = 15

# Load users from file and format them into a dictionary
def load_users():
    users = {}
    with open(LOGIN_FILE, "r") as file:
        for line in file:
            if line.strip():
                username, password = line.strip().split(",") #This formats the file into a dictionary
                users[username] = password
    return users

# Save new user to file
def save_user(username, password):
    with open(LOGIN_FILE, "a") as file:
        file.write(f"{username},{password}\n")

# Helper for non-empty input
def get_input(prompt, is_password=False):
    value = passwordbox(prompt) if is_password else enterbox(prompt)
    if value is None:  # Cancel or close
        return None
    if not value.strip():
        msgbox("Input cannot be empty. Please try again.")
        return get_input(prompt, is_password)
    return value

# Validate string length of the passsword or username, ensuring it meets the specified criteria
def valid_length(value, min_len, max_len, field_name):
    if len(value) < min_len or len(value) > max_len:
        msgbox(f"{field_name} must be between {min_len} and {max_len} characters.")
        return False
    return True

# New helper function for validation and duplicate check
def user_check(prompt, min_len, max_len, field_name, is_password=False, users=None):
    while True:
        value = get_input(prompt, is_password)
        if value is None:
            return None
        if users and value in users:
            msgbox(f"{field_name} already exists. Please choose another.")
            continue
        if not valid_length(value, min_len, max_len, field_name):
            continue
        return value

# Register a new user with validation
def register_user(users):
    # Prompt the user to enter a valid username (checks length and if already taken)
    username = user_check("Create a new username:", MIN_USER_LENGTH, MAX_USER_LENGTH, "Username", users=users)
    if username is None: 
        return False  

    # Prompt the user to create a valid password (checks length)
    password = user_check("Create a password:", MIN_PASS_LENGTH, MAX_PASS_LENGTH, "Password", is_password=True)
    if password is None:
        return False  

    # Ask the user to confirm their password
    confirm = get_input("Confirm your password:", is_password=True)
    if confirm is None:
        return False  

    # Check if the two passwords match
    if password != confirm:
        msgbox("Passwords do not match. Please try again.")
        return register_user(users)  # Recursively restart the registration process

    # Save the new user's credentials to the file and update the users dictionary
    save_user(username, password)
    users[username] = password
    return True  # Registration successful


# Login or signup interface (improved version)
def login_system():
    
    users = load_users() # Load existing users from file
    while True:
        # Display the welcome message and ask the user to log in or sign up
        action = buttonbox("Welcome to the Café App!\nDo you want to Log In or Sign Up?", "Login System", choices=["Log In", "Sign Up", "Exit"]) 
        if action == "Exit" or action is None:
            msgbox("Exiting app. Goodbye!", "Exit")
            exit()
        # If the user chooses to sign up, call the register_user function
        elif action == "Sign Up":
            if register_user(users):
                msgbox("Account created successfully!")
        # If the user chooses to log in, prompt for username and password
        elif action == "Log In":
            for attempt in range(LOGIN_ATTEMPS): # Allow up to 3 login attempts
                username = get_input("Enter your username:")    
                if username is None: #User cancelled or closed the dialog return to the main menu
                    break  
                #
                password = get_input("Enter your password:", is_password=True) 
                if password is None:
                    break
                # Check if the username and password match and if they do, welcome the user
                if users.get(username) == password: 
                    msgbox(f"Welcome, {username}!")
                    return  # Successful login
                msgbox("Incorrect username or password.")
            else:
                msgbox("Too many failed attempts. Exiting.")
                exit()

# Load menu items into a dictionary from the menu file
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



# Year level validation
def get_year_level():
    while True:
        year_str = enterbox("Enter your year level: ")
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

# Quantity validation
def valid_quantity(qty):
    return MIN_QUANTITY <= qty <= MAX_QUANTITY

# Function to get the user's order
def get_order(menu_items):
    cart = {}
    # Creates a list of item choices for the user to select from
    item_choices = [f"{num}. {item['name']}" for num, item in menu_items.items()]
    #adds all the items to the list for summary
    item_choices.append("Finish Order")

    while True:
        #Prompts the users to select an item to order
        choice_str = choicebox("Select an item to order:", "Make Your Order", item_choices)
        #If the user selects "Finish Order" or cancels, it breaks the loop
        if choice_str == "Finish Order" or choice_str is None:
            break
        item_number = int(choice_str.split(".")[0])
        current_qty = cart.get(item_number, 0)
        #tells the user how many they currently have and how many they can add
        qty_str = enterbox(f"You currently have {current_qty} of {menu_items[item_number]['name']}.\nEnter quantity to add ({MAX_QUANTITY - current_qty} left):")
        if qty_str is None:
            continue
        try:
            qty = int(qty_str)
            new_total = current_qty + qty
            #check if the new total exceeds the maximum allowed quantity
            if not valid_quantity(new_total):
                msgbox(f"You can only order a total of {MAX_QUANTITY} for {menu_items[item_number]['name']}.")
                continue
            cart[item_number] = new_total
            msgbox(f"Added {qty} of {menu_items[item_number]['name']} to your order. Total: {new_total}")
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
    # Iterates through the cart and calculates the total cost for each item
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
