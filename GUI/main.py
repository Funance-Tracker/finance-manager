import tkinter as tk
from tkinter import ttk
from model_transaction.balance import get_balance
from GUI.home import HomePage
from GUI.currency_convert import CurrencyConvertPage
from GUI.files_reader import FilesReaderPage
from GUI.report import TransactionReportApp
from GUI.debt_plans import DebtsPlanPage  # Import the DebtsPlanPage class

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
        for F in (HomePage, CurrencyConvertPage, FilesReaderPage, DebtsPlanPage):  # Add DebtsPlanPage
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

        report_button = ttk.Button(nav_frame, text="Report", command=self.open_report)
        report_button.pack(side="left", padx=5)
        
        debts_button = ttk.Button(nav_frame, text="Debts Plan", command=lambda: self.show_frame("DebtsPlanPage"))  # Add button for DebtsPlanPage
        debts_button.pack(side="left", padx=5)

        # User info on the right
        user_info_frame = ttk.Frame(header_frame)
        user_info_frame.pack(side="right", padx=10, pady=10)

        self.username_label = ttk.Label(user_info_frame, text=f"User: {self.user_info['username']}")
        self.username_label.pack(side="right", padx=5)

        self.balance_label = ttk.Label(user_info_frame, text=f"Balance: ${self.user_info['balance']:.2f}")
        self.balance_label.pack(side="right", padx=5)

    def open_report(self):
        TransactionReportApp(self.user_info['id'])

    def update_balance_label(self):
        self.user_info['balance'] = get_balance(self.user_info['id'])
        self.balance_label.config(text=f"Balance: ${self.user_info['balance']:.2f}")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

