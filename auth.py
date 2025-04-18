import bcrypt # pip install bcrypt => bcrypt is a password hashing library
from db  import connect

# function to login user
def login_user(email, password): # with to parameters email and password
	connection = connect() # check if the connection is established
	cursor = connection.cursor() # create a cursor object to execute SQL queries

	# select the user from the database
	cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
	user = cursor.fetchone() # fetchone() returns the first row of the result set

	if not user: # check if the user exists
		print("user not found") # and print the message
		connection.close() # close the connection and return None
		return

	user_id, name, email, hashed_password = user # unpack the user tuple into variables

	# check if the password is correct using bcrypt
	# bcrypt.checkpw() takes the password and the hashed password as arguments
	if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
		print("login successful for user:", name) # print the message with the user name
		connection.close() # close the connection and return the user id
		return user_id # return the user id if the password is correct
	else:
		print("invalid password for the user.") # print the message if the password is incorrect
		connection.close() # close the connection and return None
		return None # return None if the password is incorrect

# todo ----------------------------------------------------------------------------

# function to register user
def register_user(name, email, password): # with three parameters name, email and password
	connection = connect() # check if the connection is established
	cursor = connection.cursor() # create a cursor object to execute SQL queries

	# select the user from the database using the email
	cursor.execute("select * from users where email = %s", (email,))
	existing_user = cursor.fetchone() # fetchone() returns the first row of the result set

	if existing_user: # check if the user already exists
		print("user email already exists") # and print the message
		connection.close() # close the connection and return
		return # return if the user already exists
	
	hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) # hash the password using bcrypt

	# insert the user into the database using the name, email and hashed password
	cursor.execute(
		"insert into users (name, email, password)  values (%s, %s, %s)",
		(name, email, hashed_password)
	)

	connection.commit() # commit the changes to the database
	print("user registered successfully") # print the message
	connection.close() # close the connection and return
	return # return after registering the user

# todo ----------------------------------------------------------------------------

# function to delete user
def delete_user(email): # with one parameter email
	connection = connect() # check if the connection is established
	cursor = connection.cursor() # create a cursor object to execute SQL queries

	# select the user from the database using the email
	cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
	user = cursor.fetchone() # fetchone() returns the first row of the result set

	if not user: # check if the user exists
		print("user not found") # and print the message
		connection.close() # close the connection and return None
		return # return if the user does not exist

	# delete the user from the database using the email
	cursor.execute("DELETE FROM users WHERE email = %s", (email,))
	connection.commit() # commit the changes to the database
	print("user deleted successfully") # print the message
	connection.close() # close the connection and return
	return # return after deleting the user

# todo ----------------------------------------------------------------------------

# function to print all users
def print_users(): # with no parameters
	try: 
		connection = connect() # check if the connection is established
		cursor = connection.cursor() # create a cursor object to execute SQL queries

		cursor.execute("SELECT * FROM users") # select all users from the database
		users = cursor.fetchall() # fetchall() returns all rows of the result set

		if users: # check if there are any users
			for user in users: # iterate over the users
				print("result when fetching all data for user:") # print the message
				print(user, "\n") # print each user
		else: # check if there are no users
			print("no users found") # print the message

	finally: # this block will always execute, even if an exception occurs
		if connection: # check if the connection is established
			connection.close()  # close the connection
