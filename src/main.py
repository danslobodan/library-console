import menu

print("Welcome to the library!")

nextMenu = menu.showMenu("login")
while nextMenu != "exit":
	nextMenu = menu.showMenu(nextMenu)

print("Goodbye!")