import os
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

def plot_balance_over_time(user_id, data_file_path, plot_title, ylabel, max_balance=None):
    try:
        timestamps = []
        balances = []

        with open(data_file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(' - ')
                if len(parts) < 2:
                    print(f"Skipping line due to unexpected format: {line.strip()}")
                    continue

                ts_str = parts[0].strip()
                balance_part = float(parts[1].split(': ')[-1].strip())
                try:
                    ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
                    timestamps.append(ts)
                    balances.append(balance_part)
                except ValueError as e:
                    print(f"Skipping line due to parsing error: {line.strip()}")
                    print(f"Error: {e}")

        days = [ts.replace(hour=0, minute=0, second=0, microsecond=0) for ts in timestamps]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(days, balances, marker='o', linestyle='-', color='blue', linewidth=1.5)

        ax.set_title(plot_title)
        ax.set_xlabel('Date')
        ax.set_ylabel(ylabel)
        ax.grid(True)
        fig.tight_layout()

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        if max_balance is not None:
            ax.set_ylim(0, max_balance)

        return fig

    except FileNotFoundError:
        print(f"{data_file_path} not found.")
        return None

def plot_daily_average_balance(user_id, transaction_file_path, max_balance):
    plot_title = 'Daily Average Balance'
    ylabel = 'Balance'
    return plot_balance_over_time(user_id, transaction_file_path, plot_title, ylabel, max_balance)

def plot_added_balance_over_time(user_id, balance_file_path):
    plot_title = 'Added Balance Over Time'
    ylabel = 'Balance'
    return plot_balance_over_time(user_id, balance_file_path, plot_title, ylabel)

def plot_balance_and_transactions_over_time(user_id, balance_file_path, transaction_file_path):
    try:
        balance_timestamps = []
        balance_values = []

        with open(balance_file_path, 'r') as balance_file:
            for line in balance_file:
                parts = line.strip().split(' - ')
                if len(parts) < 2:
                    print(f"Skipping line due to unexpected format: {line.strip()}")
                    continue

                ts_str = parts[0].strip()
                balance_part = float(parts[1].split(': ')[-1].strip())
                try:
                    ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
                    balance_timestamps.append(ts)
                    balance_values.append(balance_part)
                except ValueError as e:
                    print(f"Skipping line due to parsing error: {line.strip()}")
                    print(f"Error: {e}")

        balance_days = [ts.replace(hour=0, minute=0, second=0, microsecond=0) for ts in balance_timestamps]

        transaction_timestamps = []
        transaction_values = []

        with open(transaction_file_path, 'r') as transaction_file:
            for line in transaction_file:
                parts = line.strip().split(' - ')
                if len(parts) < 2:
                    print(f"Skipping line due to unexpected format: {line.strip()}")
                    continue

                ts_str = parts[0].strip()
                amount = float(parts[1].split(': ')[-1].strip())
                try:
                    ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
                    transaction_timestamps.append(ts)
                    transaction_values.append(-amount)
                except ValueError as e:
                    print(f"Skipping line due to parsing error: {line.strip()}")
                    print(f"Error: {e}")

        transaction_days = [ts.replace(hour=0, minute=0, second=0, microsecond=0) for ts in transaction_timestamps]

        all_days = sorted(set(balance_days + transaction_days))
        combined_balance = []
        combined_transactions = []

        for day in all_days:
            balance = next((val for idx, val in enumerate(balance_values) if balance_days[idx] == day), None)
            transaction = sum(val for idx, val in enumerate(transaction_values) if transaction_days[idx] == day)
            combined_balance.append(balance if balance is not None else combined_balance[-1] if combined_balance else 0)
            combined_transactions.append(transaction)

        fig, ax1 = plt.subplots(figsize=(12, 4))

        color = 'tab:green'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Balance', color=color)
        ax1.plot(all_days, combined_balance, marker='o', linestyle='-', color=color, linewidth=1.5)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Transactions', color=color)
        ax2.plot(all_days, combined_transactions, marker='s', linestyle='-', color=color, linewidth=1.5)
        ax2.tick_params(axis='y', labelcolor=color)

        ax1.set_title('Balance and Transactions Over Time')
        ax1.grid(True)
        fig.tight_layout()

        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        return fig

    except FileNotFoundError:
        print("Data file not found.")
        return None
