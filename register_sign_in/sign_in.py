import psycopg2
from psycopg2 import OperationalError
from PostgresDB.postgres_db import PostgresDB
import bcrypt
import re

def validate_email(email):
    """
    Validate the email format using a regular expression.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email):
        return True
    else:
        print("Invalid email format. Please enter a valid email address.")
        return False

def hash_password(password):
    """
    Hash the password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def sign_in(email, password):
    """
    Sign in a user with the provided email and password.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        dict or str: A dictionary containing user data if the sign-in is successful,
                    or a string indicating the error:
                    - "not_valid_email" if the email format is invalid,
                    - "not_exist" if the user does not exist,
                    - "wrong_password" if the password is incorrect,
                    - "error" if there is an error connecting to the database.
    """
    if not validate_email(email):
        return "not_valid_email"

    db = PostgresDB()
    connection = None
    cursor = None

    try:
        connection = db.get_connection()
        cursor = connection.cursor()

        # Check if the user exists with the provided email
        cursor.execute("SELECT id, username, password, email, balance FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            print(f"User with email '{email}' does not exist.")
            return "not_exist"

        # Verify the hashed password
        user_id, username, db_password, user_email, balance = user
        if not bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
            print("Incorrect password. Please try again.")
            return "wrong_password"

        # If everything is correct, user is authenticated
        user_data = {
            "id": user_id,
            "username": username,
            "email": user_email,
            "balance": balance
        }
        print(f"Welcome, {username}! You have successfully signed in.")
        return user_data

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return "error"

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("PostgreSQL connection is closed.")
