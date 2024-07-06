from PostgresDB.postgres_db import PostgresDB
from datetime import datetime
import os

def get_balance_transactions_file(user_id):
    return os.path.join(os.path.dirname(__file__), f'../data/balances/user_{user_id}_transactions.txt')

def get_balance(user_id):
    """
    Retrieve the balance of the specified user from the database.

    Args:
        user_id (int): The ID of the user whose balance is to be retrieved.

    Returns:
        float or None: The user's balance if retrieved successfully, None if there's an error.
    """
    db = PostgresDB()
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM users WHERE id = %s;", (user_id,))
        balance = cursor.fetchone()
        return balance[0] if balance else None

    except Exception as e:
        print(f"Error retrieving balance: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def write_to_balance_transactions(user_id, amount, operation):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    balance_transactions_file = get_balance_transactions_file(user_id)
    
    try:
        with open(balance_transactions_file, 'a') as file:
            file.write(f"{current_datetime} - Operation: {operation}, Amount: {amount}\n")
            print(f"Successfully wrote to {balance_transactions_file}")
    except IOError as e:
        print(f"Error writing to {balance_transactions_file}: {e}")


def add_balance(user_id, amount):
    """
    Add the specified amount to the user's balance.

    Args:
        user_id (int): The ID of the user whose balance is to be updated.
        amount (float): The amount to add to the user's balance.

    Returns:
        float or None: The new balance after adding the amount, or None if there's an error.
    """
    if amount <= 0:
        print("Amount must be greater than 0")
        return None

    db = PostgresDB()
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s;", (amount, user_id))
        connection.commit()

        new_balance = get_balance(user_id)
        return new_balance

    except Exception as e:
        print(f"Error updating balance: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
