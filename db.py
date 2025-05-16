# db.py
# about this file:
# this file contains the main function to connect to the database

import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="khedr",
        password="khedr",
        database="bank_system"
    )
