#Version 1 of the app should be a simple console program with no GUI.
#year eligibility for the app is 9-13

#Constants
YEAR_ELIGIBILITY = [9, 10, 11, 12, 13]
MENU_FILE  = "menu.txt" #Path to the menu file

year_level=int(input("Enter your year level: "))
if year_level in YEAR_ELIGIBILITY:
    print("Welcome to the café app!")
else:
    print("You are not eligible to use the app.")
    exit()


#functions to load the menu items from a text file to a dictionary
def load_menu():
    menu_items = {} #Dictionary to store menu items
    with open(MENU_FILE, "r") as file:
        for line in file:
            line = line.strip() #To help remove any spaces
            if not line or line.startswith("#"):
                continue
            number, name, price = line.split(",") #store item name and price in a list
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
            if quantity <= 0:
                print("Quantity must be at least 1.")
                continue
            cart[choice] = cart.get(choice, 0) + quantity
        except ValueError:
            print("Please enter a valid number.")
    return cart

menu_items = load_menu()
display_menu(menu_items)
