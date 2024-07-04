import psycopg2
from psycopg2 import OperationalError
from PostgresDB.postgres_db import PostgresDB
import bcrypt
import re

def validate_email(email):
    """
    Validate the format of an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email):
        return True
    else:
        print("Invalid email format. Please enter a valid email address.")
        return False

def hash_password(password):
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def register_user(username, email, password):
    """
    Register a new user in the database.

    Args:
        username (str): The username of the new user.
        email (str): The email address of the new user.
        password (str): The password of the new user.

    Returns:
        str: A message indicating the result of the registration process.
    """
    if not validate_email(email):
        return "not_valid_email"
    
    db = PostgresDB()
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        # Check if the user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            print(f"User with email '{email}' already exists.")
            return "already_exist"

        hashed_password = hash_password(password)

        # Insert new user into the database
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password),
        )
        connection.commit()

        print(f"User '{username}' registered successfully.")
        return "registered_successfully"

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return "error"

    finally:
        if cursor:
            cursor.close()
        if connection:
            db.close()
