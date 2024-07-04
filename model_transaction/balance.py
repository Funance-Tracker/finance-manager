from PostgresDB.postgres_db import PostgresDB

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
    cursor = connection.cursor()

    try:
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
            db.close()


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
        return -1

    db = PostgresDB()
    connection = db.get_connection()
    cursor = connection.cursor()

    try:
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
            db.close()
