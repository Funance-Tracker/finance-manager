from PostgresDB.postgres_db import PostgresDB

def add_new_debt(user_id, amount, description, debt_date=None):
    """
    Add a new debt record for the user.

    Args:
        user_id (int): The ID of the user.
        amount (float): The amount of the debt.
        description (str): Description of the debt.
        debt_date (str): The date and time of the debt in 'YYYY-MM-DD HH:MM:SS' format (optional).

    Returns:
        bool: True if the debt was successfully added, False otherwise.
    """
    db = PostgresDB()
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        if debt_date:
            # Insert new debt with specified date and time
            cursor.execute("INSERT INTO debts (amount, description, user_id, debt_date) VALUES (%s, %s, %s, %s)", 
                           (amount, description, user_id, debt_date))
        else:
            # Insert new debt with current date and time
            cursor.execute("INSERT INTO debts (amount, description, user_id) VALUES (%s, %s, %s)", 
                           (amount, description, user_id))

        connection.commit()
        return True

    except Exception as e:
        print(f"Error inserting data: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_debts(user_id):
    """
    Retrieve all debts for the specified user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list of tuple or None: A list of tuples containing (amount, description, debt_date) for each debt,
                               or None if there's an error.
    """
    db = PostgresDB()
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT amount, description, debt_date FROM debts WHERE user_id = %s;", (user_id,))
        debts = cursor.fetchall()
        return debts
    
    except Exception as e:
        print(f"Error retrieving debts: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def delete_debt(user_id, description):
    """
    Delete a debt record for the user and update the user's balance accordingly,
    only if the user's balance is sufficient.

    Args:
        user_id (int): The ID of the user.
        description (str): Description of the debt to delete.

    Returns:
        bool: True if the debt was successfully deleted and balance updated, False otherwise.
    """
    db = PostgresDB()
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        # Retrieve amount of the debt being deleted
        cursor.execute("SELECT amount FROM debts WHERE user_id = %s AND description = %s;", (user_id, description))
        debt_amount = cursor.fetchone()

        if not debt_amount:
            print(f"No debt found with description '{description}' for user {user_id}.")
            return False

        amount = debt_amount[0]

        # Check if user's balance is sufficient
        cursor.execute("SELECT balance FROM users WHERE id = %s;", (user_id,))
        user_balance = cursor.fetchone()[0]

        if user_balance < amount:
            print("Insufficient balance. Debt cannot be deleted.")
            return False

        # Insert a transaction record with negative amount to reflect debt deletion
        cursor.execute("INSERT INTO transactions (amount, description, user_id) VALUES (%s, %s, %s);",
                       (amount, f"Paid debt: {description}", user_id))

        # Update user's balance by subtracting the debt amount
        cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s;", (amount, user_id))

        # Delete the debt record
        cursor.execute("DELETE FROM debts WHERE user_id = %s AND description = %s;", (user_id, description))

        connection.commit()
        return True

    except Exception as e:
        print(f"Error deleting debt: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()





