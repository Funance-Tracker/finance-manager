import tkinter as tk
from tkinter import ttk, messagebox
from model_transaction.transaction import add_new_transaction, write_to_transaction_transactions
from model_transaction.balance import add_balance, write_to_balance_transactions
from model_transaction.debt import add_new_debt

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
