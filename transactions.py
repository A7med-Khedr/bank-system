import re


class TransactionManager:
	
	def __init__(self, connect_func):
		self.connect_func = connect_func

	def is_valid_email(self, email):
		email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
		return re.match(email_regex, email) is not None

	def get_account_id_by_email(self, email):
		connection = self.connect_func()
		cursor = connection.cursor()

		try:
			cursor.execute("""
				SELECT accounts.id 
				FROM accounts 
				JOIN users ON accounts.user_id = users.id 
				WHERE users.email = %s
			""", (email,))
			account_id = cursor.fetchone()
			if account_id:
				return account_id[0]
			else:
				return None
		except Exception as e:
			print("Error fetching account ID:", e)
			return None
		finally:
			connection.close()


	def create_transaction(self, sender_account_id, receiver_account_id, amount, trans_type):
		connection = self.connect_func()
		cursor = connection.cursor()

		try:
			cursor.execute(
				"INSERT INTO transactions (from_account_id, to_account_id, amount, transaction_type) VALUES (%s, %s, %s, %s)",
				(sender_account_id, receiver_account_id, amount, trans_type)
			)
			connection.commit()
			print("Transaction created successfully!")
		except Exception as e:
			print("Error creating transaction:", e)
			connection.rollback()
		finally:
			connection.close()

	def update_balance(self, account_id, new_balance):
		connection = self.connect_func()
		cursor = connection.cursor()

		try:
			cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))
			connection.commit()
			print(f"Balance updated successfully for account ID {account_id}")
		except Exception as e:
			print("Error updating balance:", e)
			connection.rollback()
		finally:
			connection.close()

	def get_balance(self, account_id):
		connection = self.connect_func()
		cursor = connection.cursor()

		try:
			cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
			balance = cursor.fetchone()
			if balance:
				return balance[0]
			else:
				print("Account not found!")
				return None
		except Exception as e:
			print("Error fetching balance:", e)
			return None
		finally:
			connection.close()

	def transfer_money(self, current_user, connect_func):
		sender_account_id = current_user
		receiver_email = input("Enter receiver email: ")

		while True:
			if not self.is_valid_email(receiver_email):
				print("Invalid email format. Please enter a valid email address.")
				continue
			break

		receiver_account_id = self.get_account_id_by_email(receiver_email)

		if not receiver_account_id:
			print("Receiver email does not exist in the system.")
			return

		while True:
			try:
				amount = float(input("Enter amount: "))
				if amount <= 0:
					print("Amount must be greater than 0.")
					continue
				break
			except ValueError:
				print("Invalid input for amount. Please enter a valid number.")

		# Check sender balance
		connection = self.connect_func()
		cursor = connection.cursor()
		cursor.execute("SELECT balance FROM accounts WHERE id = %s", (sender_account_id,))
		sender_balance = cursor.fetchone()[0]
		print(f"Sender balance: {sender_balance}")  # Debugging line

		if sender_balance < amount:
			print("Insufficient funds in your account.")
			connection.close()
			return

		trans_type = 'transfer'

		# Create transaction
		self.create_transaction(sender_account_id, receiver_account_id, amount, trans_type)

		# Update sender balance
		self.update_balance(sender_account_id, sender_balance - amount)

		# Get and update receiver balance
		receiver_balance = self.get_balance(receiver_account_id)
		if receiver_balance is not None:
			self.update_balance(receiver_account_id, receiver_balance + amount)

		connection.close()

	def get_all_transactions(self):
		connection = self.connect_func()
		cursor = connection.cursor()

		try:
			cursor.execute("SELECT * FROM transactions")
			transactions = cursor.fetchall()

			if transactions:
				print("All transactions:")
				for trans in transactions:
					trans_id, from_account_id, to_account_id, amount, date, trans_type = trans
					print(f"""
						Transaction ID: { trans_id }
						From Account:   { from_account_id }
						To Account:     { to_account_id }
						Amount:         { amount }
						Date:           { date }
						Type:           { trans_type }
						--------------------------
					""")
				return transactions
			else:
				print("\nNo transactions found. ❌")
				return None

		finally:
			connection.close()

	def get_transaction_by_id(self, trans_id):
		connection = self.connect_func()
		cursor = connection.cursor()

		try:
			cursor.execute("SELECT * FROM transactions WHERE id = %s", (trans_id,))
			transaction = cursor.fetchone()

			if transaction:
				trans_id, from_account_id, to_account_id, amount, date, trans_type = transaction
				print(f"""
					Transaction ID: { trans_id }
					From Account:   { from_account_id }
					To Account:     { to_account_id }
					Amount:         { amount }
					Date:           { date }
					Type:           { trans_type }
				""")
				return transaction
			else:
				print(f"\nNo transaction found with ID {trans_id} ❌")
				return None

		finally:
			connection.close()

	def update_transaction_type(self, trans_id, new_type):
		connection = self.connect_func()
		cursor = connection.cursor()

		try:
			cursor.execute("SELECT * FROM transactions WHERE id = %s", (trans_id,))
			transaction = cursor.fetchone()

			if transaction:
				cursor.execute("UPDATE transactions SET transaction_type = %s WHERE id = %s", (new_type, trans_id))
				connection.commit()
				print(f"Transaction type updated successfully for ID {trans_id}")
				return trans_id
			else:
				print(f"No transaction found with ID {trans_id}")
				return None

		finally:
			connection.close()

	def delete_transaction(self, trans_id):
		connection = self.connect_func()
		cursor = connection.cursor()

		try:
			cursor.execute("SELECT * FROM transactions WHERE id = %s", (trans_id,))
			transaction = cursor.fetchone()

			if transaction:
				cursor.execute("DELETE FROM transactions WHERE id = %s", (trans_id,))
				connection.commit()
				print(f"\nTransaction deleted successfully for ID {trans_id}")
				return trans_id
			else:
				print(f"\nNo transaction found with ID {trans_id}")
				return None

		finally:
			connection.close()
