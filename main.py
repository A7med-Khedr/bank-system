from auth import User
from account import Account
from transactions import TransactionManager
from db import connect

def show_menu():
    print("\n📋 Main Menu:")
    print("1. Register New User")
    print("2. Login")
    print("3. Create Bank Account")
    print("4. View All Accounts")
    print("5. Transfer Money")
    print("6. View All Transactions")
    print("7. View Transaction by ID")
    print("8. Update Transaction Type")
    print("9. Delete Transaction")
    print("0. Exit")

# 1. Register New User
def register_user():
    name = input("Enter name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    users.register(name, email, password, connect)

# 2. Login
def login_user():
    email = input("Enter email: ")
    password = input("Enter password: ")
    user = users.login(email, password, connect)
    print(user)
    return user if user else None

# 3. Create Bank Account
def create_bank_account(current_user):
    if not current_user:
        print("\n❌ - You must log in first. :)")
        return

    type = input("Enter account type: ")
    balance = float(input("Enter initial balance: "))

    
    account.create(user_id = current_user, account_type=type, initial_balance=balance)

# 4. View All Accounts
def get_all_accounts(current_user):
    if not current_user:
        print("\n❌ - You must log in first. :)")
        return
        
    account.get_all_accounts()


# 5. Transfer Money
def transfer_money(current_user):
    if not current_user:
        print("\n❌ - You must log in first. :)")
        return
    
    sender = int(input("Enter sender account number: "))
    receiver = int(input("Enter receiver account number: "))
    amount = float(input("Enter amount: "))
    trans_type = input("Enter transaction type (e.g., transfer): ")
    transactions.create_transaction(sender, receiver, amount, trans_type)


# 6. View All Transactions
def get_all_transactions(current_user):
    if not current_user:
        print("\n❌ - You must log in first. :)")
        return
    
    transactions.get_all_transactions()


# 7. View Transaction by ID
def view_transaction_by_id(current_user):
    if not current_user:
        print("\n❌ - You must log in first. :)")
        return
    trans_id = int(input("Enter transaction ID: "))
    transactions.get_transaction_by_id(trans_id)

# 8. Update Transaction Type
def update_transaction_type(current_user):
    if not current_user:
        print("\n❌ - You must log in first. :)")
        return
    
    trans_id = int(input("Enter transaction ID: "))
    new_type = input("Enter new transaction type: ")
    transactions.update_transaction_type(trans_id, new_type)

# 9. Delete Transaction
def delete_transaction(current_user):
    if not current_user:
        print("\n❌ - You must log in first. :)")
        return
    
    trans_id = int(input("Enter transaction ID to delete: "))
    transactions.delete_transaction(trans_id)

# 0. Exit Program
def exit_program():
    print("Exiting the program.")
    return False

def main():
    global users, account, transactions

    users = User(connect)
    account = Account(connect)
    transactions = TransactionManager(connect)

    current_user = None

    actions = {
        "1": register_user,
        "2": login_user,
        "3": lambda: create_bank_account(current_user),
        "4": lambda: get_all_accounts(current_user),
        "5": lambda: transfer_money(current_user),
        "6": lambda:get_all_transactions(current_user),
        "7": lambda:view_transaction_by_id(current_user),
        "8": lambda:update_transaction_type(current_user),
        "9": lambda:delete_transaction(current_user),
        "0": exit_program
    }

    while True:
        show_menu()
        choice = input("Choose an option: ")

        action = actions.get(choice, None)

        if action:
            if choice == "2":
                current_user = action()
            elif choice == "0":
                if not action():
                    break
            else:
                action()
        else:
            print("Invalid choice. Please try again.")

main()
