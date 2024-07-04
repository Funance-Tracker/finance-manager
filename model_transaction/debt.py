from PostgresDB.postgres_db import PostgresDB

def add_new_debt(user_id, amount, description):
    """
    Add a new debt record for the user.

    Args:
        user_id (int): The ID of the user.
        amount (float): The amount of the debt.
        description (str): Description of the debt.

    Returns:
        bool: True if the debt was successfully added, False otherwise.
    """
    db = PostgresDB()
    connection = db.get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO debts (amount, description, user_id) VALUES (%s, %s, %s)", (amount, description, user_id))
        connection.commit()
        return True

    except Exception as e:
        print(f"Error inserting data: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            db.close()


def get_debts(user_id):
    """
    Retrieve all debts for the specified user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list of tuple or None: A list of tuples containing (amount, description) for each debt,
                               or None if there's an error.
    """
    db = PostgresDB()
    connection = db.get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT amount, description FROM debts WHERE user_id = %s;", (user_id,))
        debts = cursor.fetchall()
        return debts
    
    except Exception as e:
        print(f"Error retrieving debts: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            db.close()
