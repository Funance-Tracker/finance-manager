import matplotlib.pyplot as plt
from datetime import datetime
import os
from PostgresDB.postgres_db import PostgresDB  # Assuming this imports your database connection
from model_transaction.balance import get_balance  # Importing your get_balance function
import matplotlib.dates as mdates

# Example: user_id can be dynamically obtained based on your application logic
user_id = 4  # Replace with actual user ID logic

# Function to get the path for balance file for a user
def get_balance_file_path(user_id):
    base_directory = os.path.dirname(__file__)  # Get current directory of this script
    data_directory = os.path.join(base_directory, "data")
    balances_directory = os.path.join(data_directory, "transactions")
    return os.path.join(balances_directory, f"user_{user_id}_transactions.txt")

# Read data from file
balance_file_path = get_balance_file_path(user_id)
timestamps = []
balances = []

with open(balance_file_path, 'r') as file:
    for line in file:
        parts = line.strip().split(' - ')
        if len(parts) < 2:
            print(f"Skipping line due to unexpected format: {line.strip()}")
            continue
        
        ts_str = parts[0].strip()
        balance_part = parts[1].split(': ')[-1].split(', ')[0].strip()  # Extract balance from the part
        try:
            ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
            balance = float(balance_part)
            timestamps.append(ts)
            balances.append(balance)
        except ValueError as e:
            print(f"Skipping line due to parsing error: {line.strip()}")
            print(f"Error: {e}")

# Filter to include only timestamps from 2024
timestamps_2024 = [ts for ts in timestamps if ts.year == 2024]
balances_2024 = [balance for ts, balance in zip(timestamps, balances) if ts.year == 2024]

# Initialize dictionaries to store hourly data
hourly_balances = {}
hourly_counts = {}

# Iterate through timestamps and balances to aggregate by hour
for ts, balance in zip(timestamps_2024, balances_2024):
    hour = ts.replace(minute=0, second=0, microsecond=0)  # Round down to the hour
    if hour not in hourly_balances:
        hourly_balances[hour] = 0.0
        hourly_counts[hour] = 0
    hourly_balances[hour] += balance
    hourly_counts[hour] += 1

# Calculate average balances for each hour
hours = sorted(hourly_balances.keys())
average_balances = [hourly_balances[hour] / hourly_counts[hour] for hour in hours]

# Get user's current balance from the database
max_balance = get_balance(user_id)
if max_balance is None:
    print(f"Failed to retrieve balance for user {user_id}. Setting max balance default to 0.")
    max_balance = 0.0

# Setting y-axis limits based on maximum balance
plt.ylim(0, max_balance)

# Plot the data as a scatter plot with lines connecting points
plt.plot(hours, average_balances, marker='s', linestyle='-', color='green', linewidth=1.5)  # 's' for square

# Formatting the plot
plt.title('Hourly Average Balance for 2024')
plt.xlabel('Date')
plt.ylabel('Balance')
plt.grid(True)
plt.tight_layout()

# Customize x-axis date formatting to show only month and year for 2024
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# Set x-axis limits to include only months of 2024
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
plt.xlim(start_date, end_date)

# Displaying the plot
plt.show()
