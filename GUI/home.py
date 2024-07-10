import tkinter as tk
from tkinter import ttk, messagebox
from model_transaction.transaction import add_new_transaction, write_to_transaction_transactions
from model_transaction.balance import add_balance, write_to_balance_transactions, get_balance
from model_transaction.debt import add_new_debt
from plotting import plot_balance_and_transactions_over_time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        self.current_canvas = None  # Track the current chart canvas

        # Configure styles
        style = ttk.Style()
        style.configure("Form.TLabelframe.Label", font=("Arial", 18, "bold"))
        style.configure("Form.TLabel", font=("Arial", 14))
        style.configure("Form.TButton", font=("Arial", 12))
        style.configure("LimeGreen.TButton", background="#32CD32", foreground="#32CD32")
        style.configure("Red.TButton", background="red", foreground="red")
        style.configure("Blue.TButton", background="blue", foreground="blue")

        # Configure grid weights for resizing
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Add Balance Form (takes full width)
        add_balance_frame = ttk.LabelFrame(self, text="Add Balance", borderwidth=2, relief="groove")
        add_balance_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(add_balance_frame, text="Amount", style="Form.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.add_balance_amount = ttk.Entry(add_balance_frame)
        self.add_balance_amount.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(add_balance_frame, text="Add", command=self.add_balance, style="LimeGreen.TButton").grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Configure grid for add_balance_frame
        add_balance_frame.columnconfigure(1, weight=1)

        # Make Transaction Form (takes full width)
        transaction_frame = ttk.LabelFrame(self, text="Make Transaction", borderwidth=2, relief="groove")
        transaction_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(transaction_frame, text="Amount", style="Form.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.transaction_amount = ttk.Entry(transaction_frame)
        self.transaction_amount.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(transaction_frame, text="Description", style="Form.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.transaction_description = ttk.Combobox(transaction_frame, values=[
            "Groceries", "Rent", "Utilities", "Entertainment", "Dining", "Travel",
            "Education", "Healthcare", "Insurance", "Miscellaneous"
        ])
        self.transaction_description.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(transaction_frame, text="Make Transaction", command=self.make_transaction, style="Red.TButton").grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Configure grid for transaction_frame
        transaction_frame.columnconfigure(1, weight=1)

        # Add Debt Form (takes full width, on a new row)
        debt_frame = ttk.LabelFrame(self, text="Add Debt", borderwidth=2, relief="groove")
        debt_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        ttk.Label(debt_frame, text="Amount", style="Form.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.debt_amount = ttk.Entry(debt_frame)
        self.debt_amount.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(debt_frame, text="Description", style="Form.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.debt_description = ttk.Entry(debt_frame)
        self.debt_description.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(debt_frame, text="Add Debt", command=self.add_debt, style="Blue.TButton").grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Configure grid for debt_frame
        debt_frame.columnconfigure(1, weight=1)

        # Display charts directly
        self.show_balance_and_transactions_over_time()

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

        # Clear entry field
        self.add_balance_amount.delete(0, tk.END)

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

        # Clear entry fields
        self.transaction_amount.delete(0, tk.END)
        self.transaction_description.set('')

    def add_debt(self):
        amount = float(self.debt_amount.get())
        description = self.debt_description.get()
        user_id = self.controller.user_info['id']
        success = add_new_debt(user_id, amount, description)
        if success:
            messagebox.showinfo("Success", "Debt added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add debt.")

        # Clear entry fields
        self.debt_amount.delete(0, tk.END)
        self.debt_description.delete(0, tk.END)

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
            canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
            self.current_canvas = canvas  # Update current canvas
        else:
            messagebox.showwarning("File Not Found", "Data files not found. No data available for plotting.")

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
