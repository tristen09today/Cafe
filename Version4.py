'''For version 4 of the café app, we will implement a login system, a menu display,
 and an order management system. '''
from easygui import *
import tkinter as tk
from tkinter import ttk
import csv
import random  # Added to generate a random order number
from datetime import datetime  # Added to get the current date and time

# Constants
YEAR_ELIGIBILITY = [9, 10, 11, 12, 13]
MAX_QUANTITY = 50
MIN_QUANTITY = 1
#constants for login and registration
MENU_FILE = "menu.txt"
LOGIN_FILE = "Login.txt"
ORDER_FILE = "orders.txt"  # Added a separate file to store orders
LOGIN_ATTEMPS = 3
MIN_PASS_LENGTH = 4
MAX_PASS_LENGTH = 15
MIN_USER_LENGTH = 3
MAX_USER_LENGTH = 15

# Global variable to track the logged-in user
current_user = None

# Load users from file and format them into a dictionary
def load_users():
    users = {}
    with open(LOGIN_FILE, "r") as file:
        for line in file:
            if line.strip() and "," in line:  # Avoid unpacking order lines
                try:
                    username, password = line.strip().split(",") # This formats the file into a dictionary
                    users[username] = password
                except ValueError:
                    continue
    return users

# Save new user to file
def save_user(username, password):
    with open(LOGIN_FILE, "a") as file:
        file.write(f"{username},{password}\n")

#checks if string length of the password or username, ensuring it meets the specified criteria
def valid_length(value, min_len, max_len, field_name):
    return min_len <= len(value) <= max_len

#The function register's a new user by collecting their details through a multienterbox.
def register_user(users):
    fields = ["New Username", "New Password", "Confirm Password", "Year Level "]
    title = "Sign Up"
    msg = "Enter your new account details:"
    values = [""] * len(fields)

    #This loop will continue until the user enters valid details or cancels the registration
    while True:
        # Display the multienterbox for user input and store the values
        values = multenterbox(msg, title, fields, values)
        if values is None:
            return False

        #uses the values entered by the user to check for errors
        username, password, confirm, year_str = values
        errmsg = "" #This variable will store any error messages that need to be displayed to the user

        # Check for empty fields and other validation errors
        for i in range(len(fields)):
            if values[i].strip() == "":
                errmsg += f'"{fields[i]}" is a required field.\n\n'

        #if username already exists, invalid length, or password mismatch, or age add to errmsg
        if username in users:
            errmsg += "Username already exists.\n\n"
        if not valid_length(username, MIN_USER_LENGTH, MAX_USER_LENGTH, "Username"):
            errmsg += f"Username must be {MIN_USER_LENGTH}-{MAX_USER_LENGTH} characters.\n\n"

        if not valid_length(password, MIN_PASS_LENGTH, MAX_PASS_LENGTH, "Password"):
            errmsg += f"Password must be {MIN_PASS_LENGTH}-{MAX_PASS_LENGTH} characters.\n\n"
        if password != confirm:
            errmsg += "Passwords do not match.\n\n"

        if not year_str.isdigit():
            errmsg += "Year level must be a number.\n\n"
        else:
            year = int(year_str)
            if year not in YEAR_ELIGIBILITY:
                errmsg += "Only students in Years 9–13 are eligible.\n\n"
        # If there are any error messages, display them and continue the loop
        if errmsg:
            msg = errmsg + "Please correct the following:"
            continue

        # If all validations pass, run the function to save the user
        save_user(username, password)
        users[username] = password
        msgbox("Account created successfully!")
        return True

# The login system function handles user login and registration
def login_system():
    global current_user
    users = load_users()
    while True:
        #if there are no users, prompt the user to sign up
        action = buttonbox("Welcome to the Café App!\nDo you want to Log In or Sign Up?", "Login System", choices=["Log In", "Sign Up", "Exit"])
        if action == "Exit" or action is None: #if the user chooses to exit, display a message and exit the app
            msgbox("Exiting app. Goodbye!", "Exit")
            exit()
        #if the user chooses to sign up, call the register_user function
        elif action == "Sign Up":
            register_user(users)
        #if the user chooses to log in, prompt them for their username and password
        elif action == "Log In":
            for attempt in range(LOGIN_ATTEMPS): # Allow up to 3 login attempts
                fields = ["Username", "Password"] #fields for username and password
                values = multenterbox("Enter your login details:", "Log In", fields)
                if values is None: #if the user cancels the login, exit the loop
                    break
                username, password = values
                #if either field is empty, display an error message and continue the loop
                if not username.strip() or not password.strip():
                    msgbox("Both fields are required.")
                    continue
                #if the username and password match, display a welcome message and exit the loop
                if users.get(username) == password:
                    current_user = username
                    msgbox(f"Welcome, {username}!")
                    return
                else:
                    #else, if the username and password do not match, display an error message
                    msgbox("Incorrect username or password.")
            else:
                msgbox("Too many failed attempts. Exiting.") #exit program after 3 failed attempts
                exit()
#loads the menu from menu.txt  
def load_menu():
    menu_items = {}
    with open(MENU_FILE, "r") as file: 
        reader = csv.reader(file) #set reader to read the file
        for row in reader:
            if not row or row[0].startswith("#"): # Skip empty lines and comments in text file
                continue
            number, name, price = row # Split row into number, name, and price
            # Convert number to integer and price to float, and store in dictionary
            menu_items[int(number)] = {"name": name.strip(), "price": float(price.strip())} 
    return menu_items

# Displays the café menu in a Tkinter window
def display_menu(menu_items):
    # Create a Tkinter window to display the menu
    root = tk.Tk()
    root.title("Café Menu for Students")
    root.geometry("350x400")

    #create the title label to its size and font
    tk.Label(root, text="Café Menu", font=("Verdana Bold", 16)).pack(pady=10)
    
    #from the number of items in the menu, create a label for each item
    for number in sorted(menu_items):
        item = menu_items[number]
        label = f"{number}. {item['name']} - ${item['price']:.2f}"
        tk.Label(root, text=label, font=("Arial", 12), anchor="w").pack(fill="x", padx=20, pady=2)
    # Create a button to close the menu window
    tk.Button(root, text="Close", command=root.destroy).pack(pady=15)

    root.mainloop()
# checks if the quantity is valid, ensuring it is within the lower and upper limits
def valid_quantity(qty):
    return MIN_QUANTITY <= qty <= MAX_QUANTITY

# this function manages the cart, allowing users to add, remove, and view items in their order
def get_order(menu_items):
    cart = {}
    # from the menu items, initialize the cart with each item set to 0
    def open_cart_manager(cart, menu_items):
        def update_summary():
            summary_text.set("")
            for number in sorted(cart):
                qty = cart[number] # Get the quantity of each item in the cart
                if qty > 0: # If the quantity is greater than 0, add it to the summary
                    item = menu_items[number]
                    summary_text.set(summary_text.get() + f"{item['name']} x{qty}\n")

        #This function adds an item to the cart, increasing its quantity by 1 if it is valid
        def add_item(num):
            new_qty = cart.get(num, 0) + 1
            if valid_quantity(new_qty):
                cart[num] = new_qty
                update_summary()
        #This function removes item from cart if it exists, decreasing its quantity by 1
        def remove_item(num):
            if cart.get(num, 0) > 0:
                cart[num] -= 1
                update_summary()

        # This function closes the cart manager window
        def finish():
            root.destroy()
        # Create the main window for the cart manager
        root = tk.Tk()
        root.title("Cart Manager")
        root.geometry("450x600")

        # Create a label for the cart manager title
        ttk.Label(root, text="Edit Your Cart", font=("Arial", 14)).pack(pady=10)
        # Create a frame for the menu items
        for number in sorted(menu_items):
            item = menu_items[number]
            row = ttk.Frame(root)
            row.pack(fill="x", padx=10, pady=2)
            ttk.Label(row, text=f"{item['name']} (${item['price']:.2f})", width=28, anchor="w").pack(side="left")
            ttk.Button(row, text="+", command=lambda n=number: add_item(n)).pack(side="left", padx=2)
            ttk.Button(row, text="-", command=lambda n=number: remove_item(n)).pack(side="left", padx=2)
        # Create a label for the cart summary
        summary_text = tk.StringVar()
        ttk.Label(root, text="Cart Summary:", font=("Arial", 12)).pack(pady=10)
        ttk.Label(root, textvariable=summary_text, justify="left").pack(pady=5)

        ttk.Button(root, text="Done", command=finish).pack(pady=15)
        #update the summary text to show the current cart items
        update_summary()
        root.mainloop() #Continues the main loop of the cart manager window until choice is made

     #This function displays the order history, showing the current items in the cart
    def show_order_history():
        if not cart:
            msgbox("No order history yet.")
            return
        history = "Your Current Order:\n"
        for number in cart: # Iterate through the cart items
            item = menu_items[number]
            qty = cart[number]
            if qty > 0: # Only show items with a quantity greater than 0
                history += f"{item['name']} x{qty}\n" #add the item name and quantity to the history
        textbox("Order History", "Previously Ordered Items", history)

    while True: # Display the cart manager options from order, histroy, and finish
        action = buttonbox("Choose an option:", "Order Menu", choices=["\U0001F6D2 Order", "\U0001F4DC Order History", "✅ Finish"])
        if action is None or action == "✅ Finish": #if the user chooses to finish or cancels, break the loop
            break
        elif action == "\U0001F6D2 Order": 
            open_cart_manager(cart, menu_items)#if users choose to order, open the cart manager window
        elif action == "\U0001F4DC Order History":
            show_order_history()#If users choose history,run function.

    return cart
#The function displays the order summary, showing the items ordered and their total cost
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

    # Generate a random order number and current time
    order_number = random.randint(10000, 99999)
    pickup_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Display the summary with the order number and pickup time
    full_summary = f"{summary}\n\nOrder Number: #{order_number}\nPickup Time: {pickup_time}"
    textbox("Order Summary", "Your Order", full_summary)

    # Save to orders file with user info
    with open(ORDER_FILE, "a") as f:
        f.write(f"{current_user},{pickup_time},#{order_number},Total=${total:.2f}\n")

'''This function is the main entry point of the program, 
calling the login system, loading the menu, displaying it,
 and managing the order process'''
def main():
    login_system()
    menu_items = load_menu()
    display_menu(menu_items)
    cart = get_order(menu_items)
    display_summary(cart, menu_items)

main()
