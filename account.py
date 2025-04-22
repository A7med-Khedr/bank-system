from datetime import datetime
from decimal import Decimal

class Account:

	def __init__(self, connect_func):
		self.connect_func = connect_func
			
	def create(self, user_id, account_type, initial_balance):
		connection = self.connect_func()
		cursor = connection.cursor()

		cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
		user = cursor.fetchone()

		if not user:
			print("user not found")
			connection.close()
			return

		cursor.execute("INSERT INTO accounts (user_id, account_type, balance, created_at) VALUES (%s, %s, %s, %s)",
						(user_id, account_type, initial_balance, datetime.now()))

		connection.commit()
		print("\naccount created successfully ✅")
		connection.close()
		return True

	def get_user_accounts(self, user_id):
		connection = self.connect_func()
		cursor = connection.cursor()

		cursor.execute("SELECT * FROM accounts WHERE user_id = %s", (user_id,))
		accounts = cursor.fetchall()

		connection.close()
		return accounts

	def update_balance(self, account_id, new_balance):
		connection = self.connect_func()
		cursor = connection.cursor()

		cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))
		connection.commit()
		print("account balance updated successfully")
		connection.close()
		return True

	def delete_account_by_user(self, user_id):
		user_accounts = self.get_user_accounts(user_id)

		if not user_accounts:
			print("⚠️ You don't have any accounts to delete.")
			return

		print("Select an account to delete:")
		for i, acc in enumerate(user_accounts):
			print(f"{i+1}. Account ID: {acc[0]}, Type: {acc[2]}, Balance: {acc[3]}")

		try:
			choice = int(input("Enter the number of the account: ")) - 1
			if choice < 0 or choice >= len(user_accounts):
				print("❌ Invalid selection.")
				return
		except ValueError:
			print("❌ Please enter a valid number.")
			return

		selected_account_id = user_accounts[choice][0]

		connection = self.connect_func()
		cursor = connection.cursor()
		cursor.execute("DELETE FROM accounts WHERE id = %s", (selected_account_id,))
		connection.commit()
		connection.close()

		print("✅ Account deleted successfully.")
		return True

	def deposit_money(self, current_user):
		user_accounts = self.get_user_accounts(current_user)

		if not user_accounts:
			print("⚠️ You don't have any accounts.")
			return

		print("\nSelect an account to deposit into:")
		for i, acc in enumerate(user_accounts):
			print(f"{i+1}. Type: {acc[2]}, Balance: {acc[3]}")

		try:
			choice = int(input("Enter the number of the account: ")) - 1
			if choice < 0 or choice >= len(user_accounts):
				print("❌ Invalid selection.")
				return
		except ValueError:
			print("❌ Please enter a valid number.")
			return

		selected_account_id = user_accounts[choice][0]

		try:
			amount = Decimal(input("Enter the amount you want to deposit: "))
			if amount <= 0:
				print("❌ Amount must be positive.")
				return
		except ValueError:
			print("❌ Invalid amount.")
			return

		connection = self.connect_func()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM accounts WHERE id = %s", (selected_account_id,))
		account = cursor.fetchone()

		if not account:
			print("Account not found.")
			connection.close()
			return

		new_balance = account[3] + amount
		self.update_balance(selected_account_id, new_balance)
		print(f"✅ Deposited { amount } successfully.")
		connection.close()
		
	def withdraw(self, current_user):
		user_accounts = self.get_user_accounts(current_user)
		
		if not user_accounts:
			print("⚠️ You don't have any accounts.")
			return

		print("Select an account to withdraw from:")
		for i, acc in enumerate(user_accounts):
			print(f"{i+1}. Type: {acc[2]}, Balance: {acc[3]}")

		try:
			choice = int(input("Enter the number of the account: ")) - 1
			if choice < 0 or choice >= len(user_accounts):
				print("❌ Invalid selection.")
				return
		except ValueError:
			print("❌ Please enter a valid number.")
			return

		selected_account = user_accounts[choice]
		selected_account_id = selected_account[0]
		current_balance = Decimal(selected_account[3])

		try:
			amount = Decimal(str(input("Enter the amount you want to withdraw: ")))
			if amount <= 0:
				print("❌ Amount must be positive.")
				return
		except:
			print("❌ Invalid amount.")
			return

		if current_balance < amount:
			print("❌ Insufficient balance.")
			return

		new_balance = current_balance - amount
		self.update_balance(selected_account_id, new_balance)
		print(f"✅ Withdrawn {amount} successfully from Account ID: {selected_account_id}")
