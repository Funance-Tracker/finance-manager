from PostgresDB.postgres_db import PostgresDB
from model_transaction.balance import get_balance
import psycopg2

def add_new_transaction(user_id, amount, description, transaction_date=None):
    """
    Add a new transaction for the user.

    Args:
        user_id (int): The ID of the user.
        amount (float): The amount of the transaction.
        description (str): The description of the transaction.
        transaction_date (str): The date and time of the transaction in 'YYYY-MM-DD HH:MM:SS' format (optional).

    Returns:
        bool: True if the transaction is successfully added, False otherwise.
    """
    current_balance = get_balance(user_id)

    if current_balance is None:
        print("Error retrieving balance. Transaction cannot be completed.")
        return False

    if amount > current_balance:
        print("Insufficient balance. Transaction cannot be completed.")
        return False

    db = PostgresDB()
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        if transaction_date:
            # Insert new transaction with specified date and time
            cursor.execute("INSERT INTO transactions (amount, description, user_id, transaction_date) VALUES (%s, %s, %s, %s)",
                           (amount, description, user_id, transaction_date))
        else:
            # Insert new transaction with current date and time
            cursor.execute("INSERT INTO transactions (amount, description, user_id) VALUES (%s, %s, %s)",
                           (amount, description, user_id))

        # Update user's balance
        cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s",
                       (amount, user_id))

        connection.commit()
        print("New transaction added successfully!")
        return True

    except psycopg2.IntegrityError as e:
        # Specific error for integrity violations (e.g., unique constraint)
        print(f"Integrity error occurred: {e}")
        return False

    except psycopg2.Error as e:
        # Catch-all for psycopg2 errors
        print(f"Database error occurred: {e}")
        return False

    except Exception as e:
        # Catch-all for other exceptions
        print(f"Unexpected error occurred: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("PostgreSQL connection is closed.")
