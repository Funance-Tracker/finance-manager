import tkinter as tk
from tkinter import messagebox
from PostgresDB.postgres_db import PostgresDB
from model_transaction.balance import get_balance, add_balance
from model_transaction.transaction import add_new_transaction
from  model_transaction.debt import add_new_debt
from report import display_transactions_page

# Replace this with your actual login logic to obtain the user_id
login_user_id = 1

def get_logged_in_user(user_id):
    """Retrieve logged-in user data from the database."""
    db = PostgresDB()
    connection = db.get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, password, balance FROM users WHERE id = %s;", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return {
                "id": user_data[0],
                "username": user_data[1],
                "password": user_data[2],
                "balance": user_data[3]
            }
        else:
            return None
    except Exception as e:
        print(f"Error retrieving user data: {e}")
        return None
    finally:
        db.close()


def retrieve_balance():
    user_id = logged_in_user["id"]
    if user_id:
        balance = get_balance(user_id)
        if balance is not None:
            balance_label.config(text=f"Balance: ${balance}")
        else:
            balance_label.config(text="No balance found for this user ID")

def add_to_user_balance():
    try:
        amount = float(amount_entry.get())  # Convert input to float
        if amount <= 0:
            messagebox.showerror("Invalid Input", "Amount must be greater than 0")
            return
        
        user_id = logged_in_user["id"]
        new_balance = add_balance(user_id, amount)
        if new_balance is not None:
            balance_label.config(text=f"Balance: ${new_balance}")
             # Clear amount entry field
            amount_entry.delete(0, tk.END)
        else:
            balance_label.config(text="Failed to update balance")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid amount")

def add_transaction():
    amount = transaction_amount_entry.get()
    description = transaction_description_entry.get()

    if not amount or not description:
        messagebox.showerror("Input Error", "Please enter both amount and description.")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showerror("Input Error", "Amount must be greater than 0.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount.")
        return

    # Retrieve current balance
    current_balance = get_balance(login_user_id)

    if current_balance is None:
        messagebox.showerror("Balance Error", "Failed to retrieve current balance.")
        return

    # Check if user has sufficient balance
    if amount > current_balance:
        messagebox.showerror("Balance Error", "Insufficient balance. Transaction cannot be completed.")
        return

    # Attempt to add transaction
    result = add_new_transaction(login_user_id, amount, description)

    if result is not False:
        messagebox.showinfo("Transaction Added", "Transaction added successfully.")

        # Clear transaction entry fields
        transaction_amount_entry.delete(0, tk.END)
        transaction_description_entry.delete(0, tk.END)
        
        # Update balance display after transaction
        retrieve_balance()
    else:
        messagebox.showerror("Transaction Error", "Failed to add transaction.")



def add_debt():
    amount = debt_amount_entry.get()
    description = debt_description_entry.get()

    if not amount or not description:
        messagebox.showerror("Input Error", "Please enter both amount and description.")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showerror("Input Error", "Amount must be greater than 0.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount.")
        return

    # Attempt to add debt
    if add_new_debt(login_user_id, amount, description):
        messagebox.showinfo("Debt Added", "Debt added successfully.")
    else:
        messagebox.showerror("Debt Error", "Failed to add debt.")

    # Clear debt entry fields
    debt_amount_entry.delete(0, tk.END)
    debt_description_entry.delete(0, tk.END)

# Example usage:
logged_in_user = get_logged_in_user(login_user_id)

if logged_in_user:
    print(f"Logged-in user data: {logged_in_user}")
else:
    print("User not found or error retrieving data")

# Example usage:
logged_in_user = get_logged_in_user(login_user_id)

if logged_in_user:
    print(f"Logged-in user data: {logged_in_user}")
else:
    print("User not found or error retrieving data")

# Tkinter GUI setup
root = tk.Tk()
root.title("User Balance Manager")
root.geometry("1600x700")

# Top frame for navigation and user info
top_frame = tk.Frame(root, pady=10, bg="lightblue")
top_frame.pack(fill="x")

# Navigation buttons
home_button = tk.Button(top_frame, text="Home", width=10, command=lambda: switch_page("Home"))
home_button.pack(side="left", padx=10, pady=5)

fea1_button = tk.Button(top_frame, text="Feature 1", width=10, command=lambda: switch_page("Feature 1"))
fea1_button.pack(side="left", padx=10, pady=5)

fea2_button = tk.Button(top_frame, text="Feature 2", width=10, command=lambda: switch_page("Feature 2"))
fea2_button.pack(side="left", padx=10, pady=5)

# User info display
user_info_frame = tk.Frame(top_frame, bg="lightblue")
user_info_frame.pack(side="right", padx=10)

username_label = tk.Label(user_info_frame, text=f"Logged in as: {logged_in_user['username']}", font=("Arial", 12), bg="lightblue")
username_label.pack(pady=5)

balance_label = tk.Label(user_info_frame, text=f"Balance: ${logged_in_user['balance']}", font=("Arial", 12), bg="lightblue")
balance_label.pack(pady=5)

# Main frames for different pages
home_frame = tk.Frame(root, bg="white")
fea1_frame = tk.Frame(root, bg="white")
fea2_frame = tk.Frame(root, bg="white")

# Home page
home_title_label = tk.Label(root, text="Home Page", font=("Arial", 20), bg="white")
home_title_label.pack(pady=20)
# Frame for adding balance
add_balance_frame = tk.Frame(home_frame, bg="white", highlightbackground="black", highlightthickness=1)
add_balance_frame.grid(row=0, column=0, padx=20, pady=20)

# Label for balance addition section
add_balance_label = tk.Label(add_balance_frame, text="Add Balance", font=("Arial", 16, "bold"), bg="white")
add_balance_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

# Entry widget for entering amount
amount_label = tk.Label(add_balance_frame, text="Amount:", font=("Arial", 12), bg="white")
amount_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

amount_entry = tk.Entry(add_balance_frame, font=("Arial", 12), width=20)
amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

# Button to add balance
add_balance_button = tk.Button(add_balance_frame, text="Add Balance", command=add_to_user_balance, font=("Arial", 12), width=15)
add_balance_button.grid(row=2, column=0, columnspan=2, pady=10)


# Frame for adding transaction
transaction_frame = tk.Frame(home_frame, bg="white", highlightbackground="black", highlightthickness=1)
# transaction_frame.pack(pady=20, padx=20)
transaction_frame.grid(row=0, column=1, padx=20, pady=20)


# Transaction amount label and entry
transaction_amount_label = tk.Label(transaction_frame, text="Transaction Amount:", font=("Arial", 14))
transaction_amount_label.grid(row=0, column=0, padx=10, pady=10)

transaction_amount_entry = tk.Entry(transaction_frame, font=("Arial", 14), width=30)
transaction_amount_entry.grid(row=0, column=1, padx=10, pady=10)

# Transaction description label and entry
transaction_description_label = tk.Label(transaction_frame, text="Description:", font=("Arial", 14))
transaction_description_label.grid(row=1, column=0, padx=10, pady=10)

transaction_description_entry = tk.Entry(transaction_frame, font=("Arial", 14), width=30)
transaction_description_entry.grid(row=1, column=1, padx=10, pady=10)

# Submit transaction button
submit_transaction_button = tk.Button(transaction_frame, text="Submit Transaction", font=("Arial", 14), width=20, command=add_transaction)
submit_transaction_button.grid(row=2, columnspan=2, pady=10)

# Frame for adding debt
debt_frame = tk.Frame(home_frame, bg="white", highlightbackground="black", highlightthickness=1)
# debt_frame.pack(pady=20, padx=20)
debt_frame.grid(row=0, column=2, padx=20, pady=20)


# Debt amount label and entry
debt_amount_label = tk.Label(debt_frame, text="Debt Amount:", font=("Arial", 14))
debt_amount_label.grid(row=0, column=0, padx=10, pady=10)

debt_amount_entry = tk.Entry(debt_frame, font=("Arial", 14), width=30)
debt_amount_entry.grid(row=0, column=1, padx=10, pady=10)

# Debt description label and entry
debt_description_label = tk.Label(debt_frame, text="Description:", font=("Arial", 14))
debt_description_label.grid(row=1, column=0, padx=10, pady=10)

debt_description_entry = tk.Entry(debt_frame, font=("Arial", 14), width=30)
debt_description_entry.grid(row=1, column=1, padx=10, pady=10)

# Submit debt button
submit_debt_button = tk.Button(debt_frame, text="Submit Debt", font=("Arial", 14), width=20, command=add_debt)
submit_debt_button.grid(row=2, columnspan=2, pady=10)

# Function to display transactions page
def display_transactions():
    display_transactions_page(login_user_id, root)

# Button to display transactions
report_button = tk.Button(home_frame, text="Transaction Report", font=("Arial", 14), width=20, command=display_transactions)
report_button.grid(row=1, column=0, padx=10, pady=10)

# Initial balance retrieval
retrieve_balance()
# Function to switch between pages
def switch_page(page_name):
    for frame in (home_frame, fea1_frame, fea2_frame):
        frame.pack_forget()

    if page_name == "Home":
        home_frame.pack(fill="both", expand=True)
        retrieve_balance()
    elif page_name == "Feature 1":
        fea1_frame.pack(fill="both", expand=True)
    elif page_name == "Feature 2":
        fea2_frame.pack(fill="both", expand=True)

# Initialize with Home page
switch_page("Home")

root.mainloop()