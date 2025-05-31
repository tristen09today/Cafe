#Version 1 of the app should be a simple console program with no GUI.
#year eligibility for the app is 9-13

#Constants
YEAR_ELIGIBILITY = [9, 10, 11, 12, 13]
MAX_QUANTITY = 50  # Maximum allowed quantity per item
MIN_QUANTITY = 1   # Minimum allowed quantity per item
MENU_FILE  = "menu.txt" #Path to the menu file

# Get year level input safely
while True:
    try:
        year_level = int(input("Enter year level: "))
        if year_level in YEAR_ELIGIBILITY:
            print("Welcome to the café app!")
            break
        else:
            print("You are not eligible to use the app!")
            continue  # ERROR: Should be `exit()` to stop the program
    except:
        print("Please enter a valid number.")  # ERROR: Too generic; should catch ValueError only



#functions to load the menu items from a text file to a dictionary
import csv

def load_menu():
    menu_items = {} # Dictionary to hold menu items
    with open(MENU_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader: # Read each row in the CSV file
            if not row or row[0].startswith("#"):
                continue
            number, name, price = row # Unpack the row into number, name, and price
            menu_items[int(number)] = {
                "name": name.strip(),
                "price": float(price.strip())
            }
    return menu_items

#function to display the menu in a nice format
def display_menu(menu_items):
    print("Café Menu:")
    #sort the menu items by number
    for number in sorted(menu_items):
        item = menu_items[number]
        print(f"{number}. {item['name']} - ${item['price']:.2f}")

# Set a maximum quantity constant

# Get user order
def get_order(menu_items):
    cart = {}
    while True:
        try:
            # ask user to enter item number and quantity
            choice = int(input("\nEnter item number to order (0 to finish): "))
            if choice == 0:  # if user enters 0, finish the order
                break
            if choice not in menu_items:  # check if item number is valid
                print("Invalid item number.")
                continue
            # ask user to enter quantity
            quantity = int(input(f"Enter quantity for {menu_items[choice]['name']}: "))
            if quantity < MIN_QUANTITY:  # lower boundary check
                print("Quantity must be at least 1.")
                continue
            elif quantity > MAX_QUANTITY:  # upper boundary check
                print(f"You can order a maximum of {MAX_QUANTITY} per item.")
                continue
            else:
                print(f"Adding {quantity} of {menu_items[choice]['name']} to your order.")
                # update cart with item number and quantity using a dictionary
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

#main program flow
menu_items = load_menu()
display_menu(menu_items)
cart = get_order(menu_items)
display_summary(cart, menu_items)


