import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PostgresDB.postgres_db import PostgresDB

def fetch_transactions(user_id):
    try:
        db = PostgresDB()
        connection = db.get_connection()
        cur = connection.cursor()

        # Execute a query to fetch transactions including transaction_date for the specified user
        cur.execute("SELECT amount, description, transaction_date FROM transactions WHERE user_id = %s", (user_id,))

        # Retrieve the results
        transactions = cur.fetchall()

        # Debugging: Print fetched transactions
        print(f"Fetched transactions for user {user_id}: {transactions}")

        # Close communication with the database
        cur.close()

        return transactions
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return []

def calculate_total(transactions):
    return sum(amount for amount, _, _ in transactions)

def display_transactions_page(user_id, root):
    transactions = fetch_transactions(user_id)
    total = calculate_total(transactions)

    # Create a new window for displaying transactions
    report_window = tk.Toplevel(root)
    report_window.title("Transaction Report")
    report_window.geometry("800x600")

    # Create the Treeview for transactions
    tree = ttk.Treeview(report_window, columns=("Amount", "Description", "Transaction Date"), show="headings")
    tree.heading("Amount", text="Amount")
    tree.heading("Description", text="Description")
    tree.heading("Transaction Date", text="Transaction Date")
    tree.pack(fill=tk.BOTH, expand=True)

    # Insert transactions into the Treeview
    for amount, description, transaction_date in transactions:
        tree.insert("", "end", values=(amount, description, transaction_date))

    # Create the total label
    total_label = tk.Label(report_window, text=f"Total: {total}")
    total_label.pack()

    # Function to download transactions
    def download_transactions_file():
        if not transactions:
            print("No transactions to download.")
            return False

        try:
            # Ask the user for a file path to save the CSV file
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

            if file_path:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    # Write header row
                    writer.writerow(["Amount", "Description", "Transaction Date"])
                    # Write each transaction row with formatted date
                    for amount, description, transaction_date in transactions:
                        formatted_date = transaction_date.strftime('%Y-%m-%d %H:%M')
                        writer.writerow([amount, description, formatted_date])
                print(f"Transactions downloaded to {file_path}")
                messagebox.showinfo("Download Successful", "Transactions downloaded successfully.")
                return True
            else:
                return False
        except Exception as e:
            print(f"Error downloading transactions: {e}")
            return False

    # Button to download transactions
    download_button = tk.Button(report_window, text="Download Transactions", command=download_transactions_file)
    download_button.pack(pady=10)

# Example usage:
if __name__ == "__main__":
    # Replace with your user_id
    user_id = 1

    # Create a Tkinter root window (main window)
    root = tk.Tk()
    root.title("Transaction App")

    # Example function call to display transaction page
    display_transactions_page(user_id, root)

    # Start the Tkinter event loop
    root.mainloop()
