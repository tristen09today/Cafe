#Version 1 of the app should be a simple console program with no GUI.
#make sure to use constants for variables that are used in the program
#year eligibility for the app is 9-13

YEAR_ELIGIBILITY = [9, 10, 11, 12, 13]

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
    for number in sorted(menu_items):
        item = menu_items[number]
        print(f"{number}. {item['name']} - ${item['price']:.2f}")
