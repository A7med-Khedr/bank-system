import bcrypt
from db import connect  # تأكد إنك عندك ملف db.py فيه دالة connect

class User:
    @staticmethod
    def login(email, password):
        connection = connect()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            print("user not found")
            connection.close()
            return

        user_id, name, email, hashed_password = user

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print("login successful for user:", name)
            connection.close()
            return user_id
        else:
            print("invalid password for the user.")
            connection.close()
            return None

    @staticmethod
    def register(name, email, password):
        connection = connect()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            print("user email already exists")
            connection.close()
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, hashed_password))

        connection.commit()
        print("user registered successfully")
        connection.close()

    @staticmethod
    def delete(email):
        connection = connect()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            print("user not found")
            connection.close()
            return

        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        connection.commit()
        print("user deleted successfully")
        connection.close()

    @staticmethod
    def print_all():
        connection = connect()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        if users:
            for user in users:
                print("User:", user)
        else:
            print("no users found")

        connection.close()
