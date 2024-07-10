import csv
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
from PostgresDB.postgres_db import PostgresDB

class TransactionReportApp(tk.Tk):
    def __init__(self, user_id):
        super().__init__()

        self.title("Transaction Report")
        
        # Center window on screen and set size
        window_width = 1250
        window_height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.user_id = user_id
        self.transactions = self.fetch_transactions()
        self.total = self.calculate_total()
        
        self.create_widgets()

    def fetch_transactions(self):
        try:
            db = PostgresDB()
            connection = db.get_connection()
            cur = connection.cursor()

            # Execute a query to fetch transactions for the specified user
            cur.execute("SELECT amount, description FROM transactions WHERE user_id = %s", (self.user_id,))

            # Retrieve the results
            transactions = cur.fetchall()

            # Debugging: Print fetched transactions
            print(f"Fetched transactions for user {self.user_id}: {transactions}")

            # Close communication with the database
            cur.close()

            return transactions
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []

    def calculate_total(self):
        return sum(amount for amount, _ in self.transactions)

    def create_widgets(self):
        # Create a style
        style = ttk.Style(self)
        
        # Configure the Treeview header font and style
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

        # Create the Treeview for transactions
        self.tree = ttk.Treeview(self, columns=("Amount", "Description"), show="headings")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")

        # Center the data in the columns
        self.tree.column("Amount", anchor=tk.CENTER)
        self.tree.column("Description", anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Insert transactions into the Treeview
        for amount, description in self.transactions:
            self.tree.insert("", "end", values=(amount, description))

        # Create the total label
        self.total_label = tk.Label(self, text=f"Total: {self.total}", font=("Arial", 28))
        self.total_label.pack()

        # Button to download transactions
        self.download_button = tk.Button(self, text="Download Transactions", command=self.download_transactions_file)
        self.download_button.pack(pady=10)

    def download_transactions_file(self):
        if not self.transactions:
            print("No transactions to download.")
            return False

        try:
            # Ask the user for a file path to save the CSV file
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

            if file_path:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Amount", "Description"])
                    writer.writerows(self.transactions)
                print(f"Transactions downloaded to {file_path}")
                messagebox.showinfo("Download Successful", "Transactions downloaded successfully.")
                return True
            else:
                return False
        except Exception as e:
            print(f"Error downloading transactions: {e}")
            return False

if __name__ == "__main__":
    user_id = 6  # Example user ID, replace with actual user ID
    app = TransactionReportApp(user_id)
    app.mainloop()
