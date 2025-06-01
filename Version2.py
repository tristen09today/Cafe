#Café Menu· Create a menu-driven program to:
#o The school café wants you to create a ‘click and collect app’ for café orders. It is an app for students of years 9-13.

#o Existing student users may log in or create an account to use the app.

#o Then the app displays menu with prices for placing orders.

#o Once user chooses items, the app displays order details - items, quantity, price and total.

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

#Display the menu.txt file
menu_file = "menu.txt"
try:
    with open(menu_file, "r") as file:
        menu = file.readlines()
except FileNotFoundError:
    print(f"Error: {menu_file} not found.")
    exit()
#Display the menu






