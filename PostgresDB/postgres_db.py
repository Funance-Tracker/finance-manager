#PostgresDB
import psycopg2
from psycopg2 import OperationalError
import sys
import os
from dotenv import load_dotenv

# Add the parent directory of PostgresDB to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

class PostgresDB:
    """
    A class to manage PostgreSQL database connections.
    """

    def __init__(self):
        self.connection = None

    def get_connection(self):
        """
        Establish and return a connection to the PostgreSQL database.
        If the connection is already open, it returns the existing connection.

        Returns:
            connection (psycopg2.extensions.connection): The database connection object.
        """
        if self.connection is None or self.connection.closed != 0:
            try:
                self.connection = psycopg2.connect(
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT'),
                    database=os.getenv('DB_NAME')
                )
                print("Connection successful!")
            except OperationalError as error:
                print(f"Error while connecting to PostgreSQL {error}")
                return None
        return self.connection

    def close(self):
        """
        Close the PostgreSQL database connection if it is open.
        """
        if self.connection and self.connection.closed == 0:
            self.connection.close()
            print("PostgreSQL connection is closed.")
