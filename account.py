from datetime import datetime

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

        if not accounts:
            print("no accounts found for this user")
        else:
            for acc in accounts:
                print(f"Account ID: {acc[0]}, Type: {acc[2]}, Balance: {acc[3]}")

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

    def delete(self, account_id):
        connection = self.connect_func()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
        connection.commit()
        print("account deleted successfully")
        connection.close()
        return True

    def get(self, account_id):
        connection = self.connect_func()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
        account = cursor.fetchone()
        connection.close()
        return account

    def deposit(self, account_id, amount):
        account = self.get(account_id)
        if not account:
            print("Account not found.")
            return False

        new_balance = account[3] + amount
        self.update_balance(account_id, new_balance)
        print(f"Deposited {amount} successfully.")
        return True

    def withdraw(self, account_id, amount):
        account = self.get(account_id)
        if not account:
            print("Account not found.")
            return False

        if account[3] < amount:
            print("Insufficient balance.")
            return False

        new_balance = account[3] - amount
        self.update_balance(account_id, new_balance)
        print(f"Withdrawn {amount} successfully.")
        return True

    def get_all_accounts(self):
        connection = self.connect_func()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        if not accounts:
            print("No accounts found.")
        else:
            for acc in accounts:
                print(f"\nAccount ID: {acc[0]}, User ID: {acc[1]}, Type: {acc[2]}, Balance: {acc[3]}, Created At: {acc[4]}")

        connection.close()
        return accounts
