import menu
# repos
import users
import admins
import credentials
import books

import session

# views
import view
import listView
import credentialView
import userView
import booksView
import searchView

ADMIN_MENU = "admin"

def AddUser():

	view.printTitle("Enter user details: ")

	cred = credentialView.getCredentials(credentials.getCredentials())
	id = listView.getId(users.getUsers())
	user = userView.getUser()

	user["username"] = cred["username"]
	user["deleted"] = False
	user["books"] = []
	credentials.add(cred["username"], cred["password"])
	users.addUser(id, user)
	print("Added user:", cred["username"])

	return ADMIN_MENU

def AddAdmin():

	view.printTitle("Enter admin details: ")

	cred = credentialView.getCredentials(credentials.getCredentials())
	id = listView.getId(admins.getAdmins())
	user = userView.getUser()

	user["username"] = cred["username"]
	credentials.add(cred["username"], cred["password"])
	admins.addAdmin(id, user)
	print("Added user:", cred["username"])

	return ADMIN_MENU

def RemoveUser():

	view.printTitle("Chose user to remove: ")
	
	activeUsers = users.getActiveUsers()
	listView.printItems(activeUsers, userView.printUser)
	id = listView.choseItem(activeUsers)
	if id == 0:
		return ADMIN_MENU

	if users.hasBooks(id):
		print("Cannot delete a user that still had books lended.")
		return ADMIN_MENU

	users.remove(id)

	return ADMIN_MENU

def AddBook():

	id = listView.getId(books.getBooks())
	book = booksView.getBook()

	books.add(id, book)
	print("Added book: ")
	booksView.printBook(id, book)

	return ADMIN_MENU

def EditBook():

	searchCriteria = [ "author" , "year" ]
	found = searchView.find("books", books.getBooks(), searchCriteria, True)
	if len(found) == 0:
		print("No books match the search criteria.")
		return ADMIN_MENU

	listView.printItems(found, booksView.printBook)
	id = listView.choseItem(found)
	if id == 0:
		print("Canceled edit.")
		return ADMIN_MENU

	book = books.getBook(id)
	view.printTitle("Editing book:")
	booksView.printBook(id, book)
	print("Press <enter> to skip.")
	
	title = view.optionalInput("Title", book["title"])
	books.updateProperty(id, "title", title)

	author = view.optionalInput("Author", book["author"])
	books.updateProperty(id, "author", author)

	year = view.optionalNumeric("Year", book["year"])
	books.updateProperty(id, "year", year)

	total = view.optionalNumeric("Total copies", book["total"])
	books.updateProperty(id, "total", total)

	available = view.optionalNumeric("Available copies", book["available"])
	while int(total) < int(available):
		print("Maximum available copies can be", total)
		available = view.optionalNumeric("Available copies", book["available"])

	book = {
		"title" : title,
		"author" : author,
		"year" : year,
		"total" : total,
		"available" : available
	}
	booksView.printBook(id, book)

	return ADMIN_MENU

def LendBook():

	criteria = [ "author" , "year" ]
	fBooks = searchView.find("books", books.getBooks(), criteria, True)
	if len(fBooks) == 0:
		return ADMIN_MENU

	listView.printItems(fBooks, booksView.printBook)
	bookID = listView.choseItem(fBooks)
	if bookID == 0:
		return ADMIN_MENU

	criteria = [ "firstname" , "lastname" ]
	fUsers = searchView.find("users", users.getUsers(), criteria, True)
	if len(fUsers) == 0:
		return ADMIN_MENU
	
	listView.printItems(fUsers, userView.printUser)
	userID = listView.choseItem(fUsers)
	if userID == 0:
		return ADMIN_MENU

	if users.addBook(userID, bookID):
		print("Lended book", bookID, "to user", userID)
	else:
		print("User has already lended that book.")

	return ADMIN_MENU

def ReturnBook():

	criteria = [ "firstname" , "lastname" ]
	fUsers = searchView.find("users", users.getUsers(), criteria, True)
	if len(fUsers) == 0:
		return ADMIN_MENU
	
	listView.printItems(fUsers, userView.printUser)
	userID = listView.choseItem(fUsers)
	if userID == 0:
		return ADMIN_MENU

	if not users.hasBooks(userID):
		print("User has not lended any books.")
		return ADMIN_MENU

	lended = users.getBooks(userID)
	bks = {}
	for id in lended:
		bks[id] = books.getBook(id)

	listView.printItems(bks, booksView.printBook)
	bookID = listView.choseItem(bks)
	if bookID == 0:
		return ADMIN_MENU

	users.removeBook(userID, bookID)
	print("Returned book", bookID, "for user", userID)

	return ADMIN_MENU

menu.registerHandler("addUser", AddUser)
menu.registerHandler("addAdmin", AddAdmin)
menu.registerHandler("removeUser", RemoveUser)
menu.registerHandler("addBook", AddBook)
menu.registerHandler("editBook", EditBook)
menu.registerHandler("lendBook", LendBook)
menu.registerHandler("returnBook", ReturnBook)