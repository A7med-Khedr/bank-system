from datetime import datetime
from db import connect

class Account:
    @staticmethod
    def create(user_id, account_type, initial_balance):
        connection = connect()
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
        print("account created successfully")
        connection.close()
        return True

    @staticmethod
    def get_user_accounts(user_id):
        connection = connect()
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

    @staticmethod
    def update_balance(account_id, new_balance):
        connection = connect()
        cursor = connection.cursor()

        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))
        connection.commit()
        print("account balance updated successfully")
        connection.close()
        return True

    @staticmethod
    def delete(account_id):
        connection = connect()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
        connection.commit()
        print("account deleted successfully")
        connection.close()
        return True

    @staticmethod
    def get(account_id):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
        account = cursor.fetchone()
        connection.close()
        return account

    @staticmethod
    def deposit(account_id, amount):
        account = Account.get(account_id)
        if not account:
            print("Account not found.")
            return False

        new_balance = account[3] + amount
        Account.update_balance(account_id, new_balance)
        print(f"Deposited {amount} successfully.")
        return True

    @staticmethod
    def withdraw(account_id, amount):
        account = Account.get(account_id)
        if not account:
            print("Account not found.")
            return False

        if account[3] < amount:
            print("Insufficient balance.")
            return False

        new_balance = account[3] - amount
        Account.update_balance(account_id, new_balance)
        print(f"Withdrawn {amount} successfully.")
        return True
