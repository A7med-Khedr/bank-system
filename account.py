from db import connect
from datetime import datetime	

class AccountManager:
	@staticmethod
	def get_account(account_id):
		if not account_id:
			print("Invalid account ID.")
			return None

		with connect() as connection:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
			return cursor.fetchone()

	@staticmethod
	def create_account(user_id, account_type, initial_balance):
		with connect() as connection:
			cursor = connection.cursor()

			cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
			user = cursor.fetchone()

			if not user:
				print("User not found.")
				return False

			cursor.execute(
				"INSERT INTO accounts (user_id, account_type, balance, created_at) VALUES (%s, %s, %s, %s)",
				(user_id, account_type, initial_balance, datetime.now())
			)

			connection.commit()
			print("Account created successfully.")
			return True

	@staticmethod
	def get_user_accounts(user_id):
		if not user_id:
			print("User ID is required.")
			return

		with connect() as connection:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM accounts WHERE user_id = %s", (user_id,))
			accounts = cursor.fetchall()

			if not accounts:
				print("No accounts found for this user.")
				return []

			for account in accounts:
				print(f"Account ID: {account[0]}, Type: {account[2]}, Balance: {account[3]}")
			
			return accounts

	@staticmethod
	def update_account_balance(account_id, new_balance):
		if not account_id:
			print("Account ID is required.")
			return False

		with connect() as connection:
			cursor = connection.cursor()
			cursor.execute(
				"UPDATE accounts SET balance = %s WHERE id = %s",
				(new_balance, account_id)
			)
			connection.commit()

		print("Account balance updated successfully.")
		return True

	@staticmethod
	def delete_account(account_id):
		if not account_id:
			print("Account ID is required.")
			return False

		with connect() as connection:
			cursor = connection.cursor()
			cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
			connection.commit()

		print("🗑️ Account deleted successfully.")
		return True

	@staticmethod
	def get_account_by_id(account_id):
		if not account_id:
			print("Account ID is required.")
			return None

		with connect() as connection:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
			account = cursor.fetchone()

			if not account:
				print("Account not found.")
				return None

			return account

	@staticmethod
	def deposit(account_id, amount):
		account = AccountManager.get_account(account_id)
		if not account:
			print("Account not found.")
			return False

		new_balance = account[3] + amount

		with connect() as connection:
			cursor = connection.cursor()
			cursor.execute(
				"UPDATE accounts SET balance = %s WHERE id = %s",
				(new_balance, account_id)
			)
			connection.commit()

		print(f"💰 Deposited {amount} successfully.")
		return True

	@staticmethod
	def withdraw(account_id, amount):
		account = AccountManager.get_account(account_id)
		if not account:
			print("Account not found.")
			return False

		if account[3] < amount:
			print("Insufficient balance.")
			return False

		new_balance = account[3] - amount

		with connect() as connection:
			cursor = connection.cursor()
			cursor.execute(
				"UPDATE accounts SET balance = %s WHERE id = %s",
				(new_balance, account_id)
			)
			connection.commit()

		print(f"💸 Withdrawn {amount} successfully.")
		return True
