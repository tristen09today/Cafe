from easygui import *
import tkinter as tk
from tkinter import ttk
import csv

# Constants
YEAR_ELIGIBILITY = [9, 10, 11, 12, 13]
MAX_QUANTITY = 50
MIN_QUANTITY = 1
MENU_FILE = "menu.txt"
LOGIN_FILE = "Login.txt"
LOGIN_ATTEMPS = 3
MIN_PASS_LENGTH = 4
MAX_PASS_LENGTH = 15
MIN_USER_LENGTH = 3
MAX_USER_LENGTH = 15

def load_users():
    users = {}
    with open(LOGIN_FILE, "r") as file:
        for line in file:
            if line.strip():
                username, password = line.strip().split(",")
                users[username] = password
    return users

def save_user(username, password):
    with open(LOGIN_FILE, "a") as file:
        file.write(f"{username},{password}\n")

def valid_length(value, min_len, max_len, field_name):
    return min_len <= len(value) <= max_len

def register_user(users):
    fields = ["New Username", "New Password", "Confirm Password", "Year Level "]
    title = "Sign Up"
    msg = "Enter your new account details:"
    values = [""] * len(fields)

    while True:
        values = multenterbox(msg, title, fields, values)
        if values is None:
            return False

        username, password, confirm, year_str = values
        errmsg = ""

        for i in range(len(fields)):
            if values[i].strip() == "":
                errmsg += f'"{fields[i]}" is a required field.\n\n'

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

        if errmsg:
            msg = errmsg + "Please correct the following:"
            continue

        save_user(username, password)
        users[username] = password
        msgbox("Account created successfully!")
        return True

def login_system():
    users = load_users()
    while True:
        action = buttonbox("Welcome to the Café App!\nDo you want to Log In or Sign Up?", "Login System", choices=["Log In", "Sign Up", "Exit"])
        if action == "Exit" or action is None:
            msgbox("Exiting app. Goodbye!", "Exit")
            exit()
        elif action == "Sign Up":
            register_user(users)
        elif action == "Log In":
            for attempt in range(LOGIN_ATTEMPS):
                fields = ["Username", "Password"]
                values = multenterbox("Enter your login details:", "Log In", fields)
                if values is None:
                    break
                username, password = values
                if not username.strip() or not password.strip():
                    msgbox("Both fields are required.")
                    continue
                if users.get(username) == password:
                    msgbox(f"Welcome, {username}!")
                    return
                else:
                    msgbox("Incorrect username or password.")
            else:
                msgbox("Too many failed attempts. Exiting.")
                exit()

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

def display_menu(menu_items):
    menu_text = "Café Menu:\n"
    for number in sorted(menu_items):
        item = menu_items[number]
        menu_text += f"{number}. {item['name']} - ${item['price']:.2f}\n"
    textbox("Menu", "Available Items", menu_text)

def valid_quantity(qty):
    return MIN_QUANTITY <= qty <= MAX_QUANTITY

def get_order(menu_items):
    cart = {}

    def open_cart_manager(cart, menu_items):
        def update_summary():
            summary_text.set("")
            for number in sorted(cart):
                qty = cart[number]
                if qty > 0:
                    item = menu_items[number]
                    summary_text.set(summary_text.get() + f"{item['name']} x{qty}\n")

        def add_item(num):
            if cart.get(num, 0) < MAX_QUANTITY:
                cart[num] = cart.get(num, 0) + 1
                update_summary()

        def remove_item(num):
            if cart.get(num, 0) > 0:
                cart[num] -= 1
                update_summary()

        def finish():
            root.destroy()

        root = tk.Tk()
        root.title("Cart Manager")
        root.geometry("450x600")

        ttk.Label(root, text="Edit Your Cart", font=("Arial", 14)).pack(pady=10)

        for number in sorted(menu_items):
            item = menu_items[number]
            row = ttk.Frame(root)
            row.pack(fill="x", padx=10, pady=2)
            ttk.Label(row, text=f"{item['name']} (${item['price']:.2f})", width=28, anchor="w").pack(side="left")
            ttk.Button(row, text="+", command=lambda n=number: add_item(n)).pack(side="left", padx=2)
            ttk.Button(row, text="-", command=lambda n=number: remove_item(n)).pack(side="left", padx=2)

        summary_text = tk.StringVar()
        ttk.Label(root, text="Cart Summary:", font=("Arial", 12)).pack(pady=10)
        ttk.Label(root, textvariable=summary_text, justify="left").pack(pady=5)

        ttk.Button(root, text="Done", command=finish).pack(pady=15)

        update_summary()
        root.mainloop()

    def show_order_history():
        if not cart:
            msgbox("No order history yet.")
            return
        history = "Your Current Order:\n"
        for number in cart:
            item = menu_items[number]
            qty = cart[number]
            if qty > 0:
                history += f"{item['name']} x{qty}\n"
        textbox("Order History", "Previously Ordered Items", history)

    while True:
        action = buttonbox("Choose an option:", "Order Menu", choices=["\U0001F6D2 Order", "\U0001F4DC Order History", "✅ Finish"])
        if action is None or action == "✅ Finish":
            break
        elif action == "\U0001F6D2 Order":
            open_cart_manager(cart, menu_items)
        elif action == "\U0001F4DC Order History":
            show_order_history()

    return cart

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

def main():
    login_system()
    menu_items = load_menu()
    display_menu(menu_items)
    cart = get_order(menu_items)
    display_summary(cart, menu_items)

main()
