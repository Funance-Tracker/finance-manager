import tkinter as tk
from tkinter import ttk, messagebox
from model_transaction.transaction import add_new_transaction, write_to_transaction_transactions
from model_transaction.balance import add_balance, write_to_balance_transactions, get_balance
from model_transaction.debt import add_new_debt
from plotting import plot_daily_average_balance, plot_added_balance_over_time, plot_balance_and_transactions_over_time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Add Balance Form
        add_balance_frame = ttk.LabelFrame(self, text="Add Balance")
        add_balance_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(add_balance_frame, text="Amount:").pack(side="left", padx=5, pady=5)
        self.add_balance_amount = ttk.Entry(add_balance_frame)
        self.add_balance_amount.pack(side="left", padx=5, pady=5)
        ttk.Button(add_balance_frame, text="Add", command=self.add_balance).pack(side="left", padx=5, pady=5)

        # Make Transaction Form
        transaction_frame = ttk.LabelFrame(self, text="Make Transaction")
        transaction_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(transaction_frame, text="Amount:").pack(side="left", padx=5, pady=5)
        self.transaction_amount = ttk.Entry(transaction_frame)
        self.transaction_amount.pack(side="left", padx=5, pady=5)

        ttk.Label(transaction_frame, text="Description:").pack(side="left", padx=5, pady=5)
        self.transaction_description = ttk.Combobox(transaction_frame, values=[
            "Groceries", "Rent", "Utilities", "Entertainment", "Dining", "Travel",
            "Education", "Healthcare", "Insurance", "Miscellaneous"
        ])
        self.transaction_description.pack(side="left", padx=5, pady=5)
        ttk.Button(transaction_frame, text="Make Transaction", command=self.make_transaction).pack(side="left", padx=5, pady=5)

        # Add Debt Form
        debt_frame = ttk.LabelFrame(self, text="Add Debt")
        debt_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(debt_frame, text="Amount:").pack(side="left", padx=5, pady=5)
        self.debt_amount = ttk.Entry(debt_frame)
        self.debt_amount.pack(side="left", padx=5, pady=5)

        ttk.Label(debt_frame, text="Description:").pack(side="left", padx=5, pady=5)
        self.debt_description = ttk.Entry(debt_frame)
        self.debt_description.pack(side="left", padx=5, pady=5)
        ttk.Button(debt_frame, text="Add Debt", command=self.add_debt).pack(side="left", padx=5, pady=5)
        
        # Button to show hourly average balance
        ttk.Button(self, text="Show transactions Over Time", command=self.show_hourly_average_balance).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Button to show added balance over time
        ttk.Button(self, text="Show Balance Over Time", command=self.show_added_balance_over_time).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(self, text="Show Balance and Transactions Over Time", command=self.show_balance_and_transactions_over_time).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        
    def add_balance(self):
        amount = float(self.add_balance_amount.get())
        user_id = self.controller.user_info['id']

        # Update balance in the database
        new_balance = add_balance(user_id, amount)
        if new_balance is None:
            messagebox.showerror("Error", "Failed to update balance.")
            return

        # Write transaction to balance.txt file
        operation = "Add Balance"
        write_to_balance_transactions(user_id, amount, operation)

        # Update GUI and show success message
        self.controller.update_balance_label()
        messagebox.showinfo("Success", "Balance updated successfully.")

    def make_transaction(self):
        amount = float(self.transaction_amount.get())
        description = self.transaction_description.get()
        user_id = self.controller.user_info['id']
        success = add_new_transaction(user_id, amount, description)
        if success:
            self.controller.update_balance_label()

            # Write transaction to transaction file
            write_to_transaction_transactions(user_id, amount, description)

            messagebox.showinfo("Success", "Transaction added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add transaction.")

    def add_debt(self):
        amount = float(self.debt_amount.get())
        description = self.debt_description.get()
        user_id = self.controller.user_info['id']
        success = add_new_debt(user_id, amount, description)
        if success:
            messagebox.showinfo("Success", "Debt added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add debt.")

    def show_hourly_average_balance(self):
        # Get user_id and balance_file_path
        user_id = self.controller.user_info['id']
        transaction_file_path = self.get_transaction_file_path(user_id)

        # Get max_balance from the database
        max_balance = get_balance(user_id)
        if max_balance is None:
            max_balance = 0.0  # Handle the case where balance retrieval fails

        # Plot the hourly average balance
        fig = plot_daily_average_balance(user_id, transaction_file_path, max_balance)
        if fig:
            # Embed Matplotlib plot into Tkinter GUI using FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        else:
            messagebox.showwarning("File Not Found", "Transaction data file not found. No data available for plotting.")

    def show_added_balance_over_time(self):
        # Get user_id and balance_file_path
        user_id = self.controller.user_info['id']
        balance_file_path = self.get_balance_file_path(user_id)

        # Plot added balance over time
        fig = plot_added_balance_over_time(user_id, balance_file_path)
        if fig:
            # Embed Matplotlib plot into Tkinter GUI using FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        else:
            messagebox.showwarning("File Not Found", "Balance data file not found. No data available for plotting.")

    def get_transaction_file_path(self, user_id):
        base_directory = os.path.dirname(__file__)  # Get current directory of this script
        data_directory = os.path.join(base_directory, "..", "data")
        transactions_directory = os.path.join(data_directory, "transactions")
        return os.path.join(transactions_directory, f"user_{user_id}_transactions.txt")

    def get_balance_file_path(self, user_id):
        base_directory = os.path.dirname(__file__)  # Get current directory of this script
        data_directory = os.path.join(base_directory, "..", "data")
        balances_directory = os.path.join(data_directory, "balances")
        return os.path.join(balances_directory, f"user_{user_id}_transactions.txt")
    

    def show_balance_and_transactions_over_time(self):
        # Get user_id, balance_file_path, and transaction_file_path
        user_id = self.controller.user_info['id']
        balance_file_path = self.get_balance_file_path(user_id)
        transaction_file_path = self.get_transaction_file_path(user_id)

        # Plot balance and transactions over time
        fig = plot_balance_and_transactions_over_time(user_id, balance_file_path, transaction_file_path)
        if fig:
            # Embed Matplotlib plot into Tkinter GUI using FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        else:
            messagebox.showwarning("File Not Found", "Data files not found. No data available for plotting.")

    # Helper methods to get file paths

    def get_transaction_file_path(self, user_id):
        base_directory = os.path.dirname(__file__)  # Get current directory of this script
        data_directory = os.path.join(base_directory, "..", "data")
        transactions_directory = os.path.join(data_directory, "transactions")
        return os.path.join(transactions_directory, f"user_{user_id}_transactions.txt")

    def get_balance_file_path(self, user_id):
        base_directory = os.path.dirname(__file__)  # Get current directory of this script
        data_directory = os.path.join(base_directory, "..", "data")
        balances_directory = os.path.join(data_directory, "balances")
        return os.path.join(balances_directory, f"user_{user_id}_transactions.txt")