from auth import Account
from account import AccountManager
from transactions import TransactionManager
from db import connect  # If you have a connect() function here

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

def register_user():
    email = input("Enter email: ")
    password = input("Enter password: ")
    account_auth.register(email, password)

def login_user():
    email = input("Enter email: ")
    password = input("Enter password: ")
    user = account_auth.login(email, password)
    if user:
        print("Login successful.")
        return user
    else:
        print("Login failed.")
        return None

def create_bank_account(current_user):
    if current_user:
        balance = float(input("Enter initial balance: "))
        account_manager.create_account(user_id=current_user[0], initial_balance=balance)
    else:
        print("You must log in first.")

def transfer_money(current_user):
    if current_user:
        sender = int(input("Enter sender account number: "))
        receiver = int(input("Enter receiver account number: "))
        amount = float(input("Enter amount: "))
        trans_type = input("Enter transaction type (e.g., transfer): ")
        transaction_manager.create_transaction(sender, receiver, amount, trans_type)
    else:
        print("You must log in first.")

def get_all_transactions():
    transaction_manager.get_all_transactions()

def view_transaction_by_id():
    trans_id = int(input("Enter transaction ID: "))
    transaction_manager.get_transaction_by_id(trans_id)

def update_transaction_type():
    trans_id = int(input("Enter transaction ID: "))
    new_type = input("Enter new transaction type: ")
    transaction_manager.update_transaction_type(trans_id, new_type)

def delete_transaction():
    trans_id = int(input("Enter transaction ID to delete: "))
    transaction_manager.delete_transaction(trans_id)

def exit_program():
    print("Exiting the program.")
    return False

def main():
    global account_auth, account_manager, transaction_manager
    account_auth = Account(connect)
    account_manager = AccountManager(connect)
    transaction_manager = TransactionManager(connect)

    current_user = None

    # Switch case dictionary
    actions = {
        "1": register_user,
        "2": login_user,
        "3": lambda: create_bank_account(current_user),
        "4": account_manager.get_all_accounts,
        "5": lambda: transfer_money(current_user),
        "6": get_all_transactions,
        "7": view_transaction_by_id,
        "8": update_transaction_type,
        "9": delete_transaction,
        "0": exit_program
    }

    while True:
        show_menu()
        choice = input("Choose an option: ")

        # Call the function corresponding to the choice
        action = actions.get(choice, None)

        if action:
            # Perform action
            if choice == "2":  # Login action changes current_user
                current_user = action()
            else:
                action()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
