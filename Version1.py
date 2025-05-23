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