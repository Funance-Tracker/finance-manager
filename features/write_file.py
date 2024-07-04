import os
from PostgresDB.postgres_db import PostgresDB

def save_transactions_to_file(user_id, file_path):
    """
    Retrieves transactions for a specific user from the database and saves them to a CSV file.

    Args:
        user_id (int): The ID of the user whose transactions are to be retrieved.
        file_path (str): The path to the CSV file where transactions will be saved.

    """
    db = PostgresDB()
    connection = db.get_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT amount, description 
        FROM transactions 
        WHERE user_id = %s;
        """
        cursor.execute(query, (user_id,))
        transactions = cursor.fetchall()

        with open(file_path, 'w') as file:
            for amount, description in transactions:
                file.write(f"{amount},{description}\n")
        print(f"Transactions saved to {file_path}")

    except Exception as e:
        print(f"Error retrieving or saving transactions: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            db.close()
