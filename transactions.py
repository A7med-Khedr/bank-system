from db import connect
class TransactionManager:

	def __init__(self, connect_func):
		self.connect_func = connect_func

	def create_transaction(self, sender_account_id, receiver_account_id, amount, transaction_type):
		connection = self.connect_func()
		cursor = connection.cursor()

		try:
			if sender_account_id == receiver_account_id:
				print("Cannot transfer to the same account.")
				return None

			# Check sender account
			cursor.execute("SELECT balance FROM accounts WHERE id = %s", (sender_account_id,))
			sender_balance = cursor.fetchone()
			if not sender_balance:
				print("Sender account does not exist.")
				return None

			# Check receiver account
			cursor.execute("SELECT balance FROM accounts WHERE id = %s", (receiver_account_id,))
			receiver_balance = cursor.fetchone()
			if not receiver_balance:
				print("Receiver account does not exist.")
				return None

			if amount <= 0:
				print("Amount must be greater than 0.")
				return None

			if sender_balance[0] < amount:
				print("Insufficient balance.")
				return None

			# Perform transaction
			cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, sender_account_id))
			cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, receiver_account_id))

			# Record transaction
			cursor.execute("""
				INSERT INTO transactions (sender_account_id, receiver_account_id, amount, transaction_type)
				VALUES (%s, %s, %s, %s)
			""", (sender_account_id, receiver_account_id, amount, transaction_type))

			connection.commit()
			print("Transaction successful.")
			return True

		except Exception as e:
			connection.rollback()
			print("Transaction failed:", e)
			return None

		finally:
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
