import bcrypt
from db import connect

class User:

	def __init__(self, connect_func):
		self.connect_func = connect_func

	def login(self, email, password, connect_func):
		connection = self.connect_func()
		cursor = connection.cursor()

		cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
		user = cursor.fetchone()

		if not user:
			print("user not found")
			connection.close()
			return

		user_id, name, email, hashed_password = user

		if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
			print("\n✅ login successful")
			connection.close()
			return user_id
		else:
			print("❌ invalid password for the user.")
			connection.close()
			return None

	def register(self, name, email, password, connect_func):
		connection = self.connect_func()
		cursor = connection.cursor()

		cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
		existing_user = cursor.fetchone()

		if existing_user:
			print("user email already exists")
			connection.close()
			return

		hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

		cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
						(name, email, hashed_password))

		connection.commit()
		print("user registered successfully ✅")
		connection.close()

	def delete(self, email, connect_func):
		connection = self.connect_func()
		cursor = connection.cursor()

		cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
		user = cursor.fetchone()

		if user:
			user_id = user[0]

			cursor.execute("DELETE FROM accounts WHERE user_id = %s", (user_id,))

			cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

			connection.commit()
			print("✅ User and their accounts deleted successfully.")
		else:
			print("⚠️ User not found.")

	def print_all(self):
		connection = self.connect_func()
		cursor = connection.cursor()

		cursor.execute("SELECT * FROM users")
		users = cursor.fetchall()

		if users:
			for user in users:
				print("User:", user)
		else:
			print("no users found")

		connection.close()

	def get_all_users(connect_func):
		connection = connect_func()
		cursor = connection.cursor()

		try:
			cursor.execute("SELECT id, name, email, balance FROM users")
			users = cursor.fetchall()

			if users:
				print("All Users:\n")
				for user in users:
					user_id, name, email, balance = user
					print(f"""
						ID:      { user_id }
						Name:    { name }
						Email:   { email }
						Balance: { balance }
						-----------------------------
					""")
			else:
				print("No users found in the system.")

			return users
		except Exception as e:
			print("Error while fetching users:", e)
			return []
		finally:
			connection.close()
