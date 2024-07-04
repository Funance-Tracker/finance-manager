import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from features.api import fetch_data, convert
from features.read_file import read_csv_file, plot_column_chart
from features.write_file import save_transactions_to_file
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model_transaction.balance import get_balance, add_balance
from model_transaction.debt import add_new_debt
from model_transaction.transaction import add_new_transaction

class Home(tk.Tk):
    def __init__(self, user_info):
        super().__init__()

        self.title("Finance Manager")
        
        # Center window on screen and set size
        window_width = 1250
        window_height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.user_info = user_info  # Store user_info for later use in the class

        # Create header frame
        self.create_header()
        
        # Create main container for frames
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill="both", expand=True)

        # Create frames for each page
        self.frames = {}
        for F in (HomePage, CurrencyConvertPage, FilesReaderPage):
            page_name = F.__name__
            frame = F(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x")

        # Navigation buttons on the left
        nav_frame = ttk.Frame(header_frame)
        nav_frame.pack(side="left", padx=10, pady=10)

        home_button = ttk.Button(nav_frame, text="Home", command=lambda: self.show_frame("HomePage"))
        home_button.pack(side="left", padx=5)

        currency_button = ttk.Button(nav_frame, text="Currency Convert", command=lambda: self.show_frame("CurrencyConvertPage"))
        currency_button.pack(side="left", padx=5)

        files_button = ttk.Button(nav_frame, text="Files Reader", command=lambda: self.show_frame("FilesReaderPage"))
        files_button.pack(side="left", padx=5)

        # User info on the right
        user_info_frame = ttk.Frame(header_frame)
        user_info_frame.pack(side="right", padx=10, pady=10)

        self.username_label = ttk.Label(user_info_frame, text=f"User: {self.user_info['username']}")
        self.username_label.pack(side="right", padx=5)

        self.balance_label = ttk.Label(user_info_frame, text=f"Balance: ${self.user_info['balance']:.2f}")
        self.balance_label.pack(side="right", padx=5)

    def update_balance_label(self):
        self.user_info['balance'] = get_balance(self.user_info['id'])
        self.balance_label.config(text=f"Balance: ${self.user_info['balance']:.2f}")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Add Balance Form
        add_balance_frame = ttk.LabelFrame(self, text="Add Balance")
        add_balance_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(add_balance_frame, text="Amount:").pack(side="left", padx=5, pady=5)
        self.add_balance_amount = ttk.Entry(add_balance_frame)
        self.add_balance_amount.pack(side="left", padx=5, pady=5)
        ttk.Button(add_balance_frame, text="Add", command=self.add_balance).pack(side="left", padx=5, pady=5)

        # Make Transaction Form
        transaction_frame = ttk.LabelFrame(self, text="Make Transaction")
        transaction_frame.pack(fill="x", padx=10, pady=10)

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
        debt_frame.pack(fill="x", padx=10, pady=10)

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
        new_balance = add_balance(user_id, amount)
        if new_balance is not None:
            self.controller.update_balance_label()
            messagebox.showinfo("Success", "Balance updated successfully.")
        else:
            messagebox.showerror("Error", "Failed to update balance.")

    def make_transaction(self):
        amount = float(self.transaction_amount.get())
        description = self.transaction_description.get()
        user_id = self.controller.user_info['id']
        success = add_new_transaction(user_id, amount, description)
        if success:
            self.controller.update_balance_label()
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

class CurrencyConvertPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.data = fetch_data()

        label = ttk.Label(self, text="Currency Convert")
        label.pack(pady=10, padx=10)

        # Currency Conversion Form
        convert_frame = ttk.LabelFrame(self, text="Currency Conversion")
        convert_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(convert_frame, text="Amount in JOD:").pack(side="left", padx=5, pady=5)
        self.amount_entry = ttk.Entry(convert_frame)
        self.amount_entry.pack(side="left", padx=5, pady=5)

        ttk.Label(convert_frame, text="To Currency:").pack(side="left", padx=5, pady=5)
        self.to_currency_var = tk.StringVar(value='USD')  # Set default value to USD
        self.to_currency_dropdown = ttk.Combobox(convert_frame, textvariable=self.to_currency_var, values=list(self.data.keys()))
        self.to_currency_dropdown.pack(side="left", padx=5, pady=5)

        self.convert_button = ttk.Button(convert_frame, text="Convert", command=self.convert_currency)
        self.convert_button.pack(side="left", padx=5, pady=5)

        self.result_label = ttk.Label(convert_frame, text="")
        self.result_label.pack(side="left", padx=5, pady=5)

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            to_currency = self.to_currency_var.get()
            from_currency = 'JOD'  # Fixed 'JOD' as the source currency
            converted_amount = convert(amount, from_currency, to_currency, self.data)
            if converted_amount is not None:
                self.result_label.config(text=f"{amount:.2f} {from_currency} is equivalent to {converted_amount:.2f} {to_currency}")
            else:
                messagebox.showerror("Conversion Error", f"Conversion failed for {from_currency} to {to_currency}.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

class FilesReaderPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Files Reader")
        label.pack(pady=10, padx=10)

        # File Reader Form
        file_reader_frame = ttk.LabelFrame(self, text="Upload and Plot CSV File")
        file_reader_frame.pack(fill="x", padx=10, pady=10)

        self.upload_button = ttk.Button(file_reader_frame, text="Upload CSV", command=self.upload_and_plot)
        self.upload_button.pack(side="left", padx=5, pady=5)

        self.summary_label = ttk.Label(file_reader_frame, text="", padding=10, justify=tk.LEFT, font=("Helvetica", 15))
        self.summary_label.pack(side="left", padx=5, pady=5)

        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def upload_and_plot(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                data = read_csv_file(file_path)
                self.display_transaction_summary(data)
                self.plot_column_chart_in_tkinter(data)
            except Exception as e:
                messagebox.showerror("Error", f"Error processing file: {e}")

    def display_transaction_summary(self, data):
        total, summary = self.calculate_transaction_summary(data)

        summary_text = f"Total: {total:.2f} JD\n\n"
        for category, amount in summary.items():
            summary_text += f"Category: {category}, Amount: {amount:.2f} JD\n"

        self.summary_label.config(text=summary_text)

    def calculate_transaction_summary(self, data):
        summary = {}
        total = 0.0

        for amount, category in data:
            if category in summary:
                summary[category] += amount
            else:
                summary[category] = amount
            total += amount
        
        return total, summary

    def plot_column_chart_in_tkinter(self, data):
        if not data:
            messagebox.showwarning("No Data", "No data to plot.")
            return

        figure = plt.Figure(figsize=(5, 4))
        ax = figure.add_subplot(111)

        amounts, categories = zip(*data)
        ax.bar(categories, amounts, color='skyblue')
        ax.set_xlabel('Categories')
        ax.set_ylabel('Amount')
        ax.set_title('Amount by Category')
        ax.tick_params(axis='x', rotation=45)
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# if __name__ == "__main__":
#     user_info = {
#         "id": 1,
#         "username": "john_doe",
#         "balance": 100.00
#     }
#     app = Home(user_info)
#     app.mainloop()
