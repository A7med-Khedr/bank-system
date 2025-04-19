# System Bank Online

## Description

System Bank Online is a simple banking system that allows users to create accounts, deposit and withdraw money, and perform transactions. It includes functionalities such as user account management and transaction processing with a MySQL database and Python backend.

## Features

- **Account Management:**
  - Create new accounts.
  - View user accounts.
  - Update account balances.
  - Delete accounts.
  - Deposit and withdraw money.
  
- **Transaction Management:**
  - Create transactions between accounts.
  - View all transactions.
  - Update transaction types.
  - Delete transactions.
  
- **User Authentication:**
  - Secure account creation and password handling using `bcrypt` (if implemented in the future).
  
## Technologies

- **Python:** Backend for handling business logic and database connections.
- **MySQL:** Database to store user and account information, as well as transactions.
- **bcrypt:** For securely hashing user passwords (if implemented).
- **datetime:** To handle timestamps for account creation and transactions.

## Setup

### Prerequisites

- Python 3.x
- MySQL Server
- Install dependencies via `pip`

### Installation Steps

1. **Clone the repo:**

   ```bash
   git clone https://github.com/A7med-Khedr/bank-system.git
   cd system-bank-online
