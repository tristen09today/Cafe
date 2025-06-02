# Version 2 of the app should be more complex involving Easy GUI 
# Year eligibility for the app is 9-13
from easygui import *
# Constants
YEAR_ELIGIBILITY = [9, 10, 11, 12, 13]
MAX_QUANTITY = 50  # Maximum allowed quantity per item
MIN_QUANTITY = 1   # Minimum allowed quantity per item
MENU_FILE  = "menu.txt"  # Path to the menu file

# Get year level input safely
while True:
    try:
        year_level = int(input("Enter year level: "))
        if year_level in YEAR_ELIGIBILITY:
            print("Welcome to the café app!")
            break
        else:
            print("You are not eligible to use the app!")
            exit()
    except ValueError:
        print("Please enter a valid number.")  # More specific error handling

# Function to load the menu items from a text file to a dictionary
import csv

def load_menu():
    menu_items = {}  # Dictionary to hold menu items
    with open(MENU_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:  # Read each row in the CSV file
            if not row or row[0].startswith("#"):
                continue
            number, name, price = row  # Unpack the row into number, name, and price
            menu_items[int(number)] = {
                "name": name.strip(),
                "price": float(price.strip())
            }
    return menu_items

# Function to display the menu in a nice format
def display_menu(menu_items):
    print("Café Menu:")
    for number in sorted(menu_items):
        item = menu_items[number]
        print(f"{number}. {item['name']} - ${item['price']:.2f}")

#Reusable quantity validation function
def is_valid_quantity(qty):
    return MIN_QUANTITY <= qty <= MAX_QUANTITY

# Get user order
def get_order(menu_items):
    cart = {}
    while True:
        try:
            choice = int(input("\nEnter item number to order (0 to finish): "))
            if choice == 0:
                break
            if choice not in menu_items:
                print("Invalid item number.")
                continue
            quantity = int(input(f"Enter quantity for {menu_items[choice]['name']}: "))
            if not is_valid_quantity(quantity):
                print(f"Quantity must be between {MIN_QUANTITY} and {MAX_QUANTITY}.")
                continue
            print(f"Adding {quantity} of {menu_items[choice]['name']} to your order.")
            cart[choice] = cart.get(choice, 0) + quantity
        except ValueError:
            print("Please enter a valid number.")
    return cart

# Display summary
def display_summary(cart, menu_items):
    print("\nOrder Summary:")
    total = 0
    for number, quantity in cart.items():
        item = menu_items[number]
        cost = item["price"] * quantity
        print(f"{item['name']} x{quantity} = ${cost:.2f}")
        total += cost
    print(f"Total Price: ${total:.2f}")

# Main program flow
menu_items = load_menu()
display_menu(menu_items)
cart = get_order(menu_items)
display_summary(cart, menu_items)



