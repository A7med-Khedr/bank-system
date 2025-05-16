from auth import User
from account import Account
from transactions import TransactionManager
from db import connect
import tkinter as tk
from tkinter import ttk
from gui import show_transactions, add_transaction

"""
    in database:
        - users table:
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                password VARCHAR(100),
                balance FLOAT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

        - transactions table:

            CREATE TABLE transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                type ENUM('deposit', 'withdraw', 'transfer'),
                amount FLOAT,
                target_user_id INT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (target_user_id) REFERENCES users(id)
            );

        - accounts table:
            CREATE TABLE accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                account_type VARCHAR(50) NOT NULL,
                balance DECIMAL(10, 2) NOT NULL,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

    libraries:
        - mysql-connector-python => pip install mysql-connector-python
        - bcrypt => command: pip install bcrypt
"""

def show_menu():
    print("===== Bank System CLI =====")
    print("1. User Operations")
    print("2. Account Operations")
    print("3. Transaction Operations")
    print("0. Exit")
    print("===========================")

def user_menu():
    print("===== User Operations =====")
    print("1. Register New User") 
    print("2. Login")
    print("3. Delete User") 
    print("0. Back to Main Menu")
    print("===========================")

def account_menu():
    print("===== Account Operations =====")
    print("1. Create Bank Account")
    print("2. View All Accounts")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Delete Account")
    print("0. Back to Main Menu")
    print("==============================")

def transaction_menu():
    print("===== Transaction Operations =====")
    print("1. Transfer Money") 
    print("2. View All Transactions")
    print("0. Back to Main Menu")
    print("===============================")

def require_login(user):
    if not user:
        print("❌ - You must log in first.")
        return False
    return True

def register_user():
    name = input("Enter name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    users.register(name, email, password, connect)

def login_user():
    email = input("Enter email: ")
    password = input("Enter password: ")
    user = users.login(email, password, connect)
    return user if user else None

def delete_user():
    email = input("Enter email of the user to delete: ")
    users.delete(email, connect)

def create_bank_account(current_user):
    if not require_login(current_user):
        return

    type = input("Enter account type: ")
    balance = float(input("Enter initial balance: "))

    
    account.create(user_id = current_user, account_type=type, initial_balance=balance)

def deposit_money(current_user):
    if not require_login(current_user):
        return

    account.deposit_money(current_user)

def withdraw_money(current_user):
    if not require_login(current_user):
        return

    account.withdraw(current_user)

def delete_account(current_user):
	if not require_login(current_user):
		return

	account.delete_account_by_user(current_user)

def get_accounts(current_user):
    if not require_login(current_user):
        return
    
    account.get_user_accounts(current_user)

def transfer(current_user):
    if not require_login(current_user):
        return
    
    transactions.transfer_money(current_user, connect)

def get_all_transactions(current_user):
    if not require_login(current_user):
        return
    
    transactions.get_all_transactions()

# def view_transaction_by_id(current_user):
    if not require_login(current_user):
        return
    
    trans_id = int(input("Enter transaction ID: "))
    transactions.get_transaction_by_id(trans_id)

def show_all_users():
    User.get_all_users(connect)

def exit_program():
    print("Exiting the program.")
    return False

def main():
    global users, account, transactions

    users = User(connect)
    account = Account(connect)
    transactions = TransactionManager(connect)

    current_user = None

    while True:
        show_menu()
        choice = input("Choose an option: ")

        match choice:
            case "1":
                # User operations menu
                while True:
                    user_menu()
                    user_choice = input("Choose a user operation: ")

                    match user_choice:
                        case "1":
                            register_user()
                        case "2":
                            current_user = login_user()
                        case "3":
                            delete_user()
                        case "0":
                            break
                        case _:
                            print("⚠️ Invalid choice. Please try again.")

            case "2":
                # Account operations menu
                while True:
                    account_menu()
                    acc_choice = input("Choose an account operation: ")

                    match acc_choice:
                        case "1":
                            create_bank_account(current_user)
                        case "2":
                            get_accounts(current_user)
                        case "3":
                            deposit_money(current_user)
                        case "4":
                            withdraw_money(current_user)
                        case "5":
                            delete_account(current_user)
                        case "0":
                            break
                        case _:
                            print("⚠️ Invalid choice. Please try again.")

            case "3":
                # Transaction operations menu
                while True:
                    transaction_menu()
                    trans_choice = input("Choose a transaction operation: ")

                    match trans_choice:
                        case "1":
                            transfer(current_user)
                        case "2":
                            get_all_transactions(current_user)
                        case "0":
                            break
                        case _:
                            print("⚠️ Invalid choice. Please try again.")

            case "0":
                print("👋 Exiting program. Goodbye!")
                break

            case _:
                print("⚠️ Invalid main choice. Please try again.")

main()

# show_all_users()

transactions = [
    {"transaction_id": 1, "date": "2025-04-20", "amount": 500, "type": "Deposit", "from_account": "12345", "to_account": "67890"},
    {"transaction_id": 2, "date": "2025-04-21", "amount": 300, "type": "Withdrawal", "from_account": "67890", "to_account": "12345"},
    {"transaction_id": 3, "date": "2025-04-22", "amount": 1500, "type": "Deposit", "from_account": "11223", "to_account": "44556"},
]

root = tk.Tk()
root.title("System Bank - Transactions")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=20)

tree = ttk.Treeview(frame, columns=("Transaction ID", "Date", "Amount", "Type", "From Account", "To Account"), show="headings")
tree.heading("Transaction ID", text="Transaction ID")
tree.heading("Date", text="Date")
tree.heading("Amount", text="Amount")
tree.heading("Type", text="Type")
tree.heading("From Account", text="From Account")
tree.heading("To Account", text="To Account")
tree.pack(fill=tk.BOTH, expand=True)

frame2 = tk.Frame(root)
frame2.pack(pady=20)

label_from_account = tk.Label(frame2, text="From Account:")
label_from_account.grid(row=0, column=0, padx=10, pady=5)
entry_from_account = tk.Entry(frame2)
entry_from_account.grid(row=0, column=1, padx=10, pady=5)

label_to_account = tk.Label(frame2, text="To Account:")
label_to_account.grid(row=1, column=0, padx=10, pady=5)
entry_to_account = tk.Entry(frame2)
entry_to_account.grid(row=1, column=1, padx=10, pady=5)

label_amount = tk.Label(frame2, text="Amount:")
label_amount.grid(row=2, column=0, padx=10, pady=5)
entry_amount = tk.Entry(frame2)
entry_amount.grid(row=2, column=1, padx=10, pady=5)

button_add_transaction = tk.Button(frame2, text="Add Transaction", command=lambda: add_transaction(entry_from_account, entry_to_account, entry_amount, transactions, tree))
button_add_transaction.grid(row=3, columnspan=2, pady=20)

button_show_transactions = tk.Button(root, text="Show Transactions", command=lambda: show_transactions(tree, transactions))
button_show_transactions.pack(pady=20)
show_transactions(tree, transactions)

root.mainloop()
