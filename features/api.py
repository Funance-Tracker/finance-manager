import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key from environment variables
API_KEY = os.getenv('API_KEY')

# Base URL for currency API
BASE_URL = f'https://api.currencyapi.com/v3/latest?apikey={API_KEY}'

def fetch_data():
    """
    Fetches the latest currency exchange rate data from the API.

    Returns:
        dict or None: Dictionary containing currency data if successful, None if an error occurs.
    """
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get('data')  # Return data['data'] if available, else None
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def convert(amount, from_currency, to_currency, data):
    """
    Converts an amount from one currency to another using the provided data.

    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency code to convert from.
        to_currency (str): The currency code to convert to.
        data (dict): Dictionary containing currency exchange rate data.

    Returns:
        float or None: The converted amount if successful, None if an error occurs.
    """
    if from_currency not in data or to_currency not in data:
        print(f"Data for {from_currency} or {to_currency} not found.")
        return None

    try:
        converted_amount = amount / data[from_currency]['value'] * data[to_currency]['value']
        return converted_amount
    except KeyError as e:
        print(f"Error converting amount: {e}")
        return None
