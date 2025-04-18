# db.py
import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="khedr",
        password="khedr",
        database="bank_system"
    )
