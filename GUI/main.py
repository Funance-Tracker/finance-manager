import tkinter as tk
from tkinter import ttk
from GUI.home import HomePage
from GUI.currency_convert import CurrencyConvertPage
from GUI.debt_plans import DebtsPlanPage
from GUI.side_buttons import SideButtons
from model_transaction.balance import get_balance
class Home(tk.Tk):
    def __init__(self, user_info):
        super().__init__()

        self.title("Finance Manager")
        
        # Maximize the window and keep the title bar and exit button visible
        self.state('zoomed')

        self.user_info = user_info  # Store user_info for later use in the class

        # Create header frame
        self.create_header()

        # Main container for frames
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill="both")

        self.main_container.grid_rowconfigure(0, weight=2)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=2)

        # Side buttons frame on the left
        self.side_buttons = SideButtons(self.main_container, self)
        self.side_buttons.grid(row=1, column=0, sticky="ns")

        # Frame for pages on the right
        self.pages_container = ttk.Frame(self.main_container)
        self.pages_container.grid(row=1, column=1, sticky="nsew")

        # Create frames for each page
        self.frames = {}
        for F in (HomePage, CurrencyConvertPage, DebtsPlanPage):
            page_name = F.__name__
            frame = F(parent=self.pages_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 40))

        # Navigation buttons on the left
        nav_frame = ttk.Frame(header_frame)
        nav_frame.pack(side="left", padx=10, pady=10)

        style = ttk.Style(self)
        style.configure("Green.TButton", background="green", foreground="green", font=("Helvetica", 16))

        home_button = ttk.Button(nav_frame, text="Home", style="Green.TButton" ,command=lambda: self.show_frame("HomePage"))
        home_button.pack(side="left", padx=(20,10), pady=(20, 5))

        currency_button = ttk.Button(nav_frame, text="Currency Convert", style="Green.TButton" ,command=lambda: self.show_frame("CurrencyConvertPage"))
        currency_button.pack(side="left", padx=(10,10), pady=(20,5))
        
        debts_button = ttk.Button(nav_frame, text="Debts Plan", style="Green.TButton" ,command=lambda: self.show_frame("DebtsPlanPage"))
        debts_button.pack(side="left", padx=(10,10), pady=(20,5))

        # User info on the right
        user_info_frame = ttk.Frame(header_frame)
        user_info_frame.pack(side="right", padx=10, pady=10)

        # Create a style
        style = ttk.Style(self)

        # Configure the Label style
        style.configure("Green.TLabel", foreground="green", font=("Helvetica", 14, "bold"))

        self.username_label = ttk.Label(user_info_frame, text=f"User: {self.user_info['username']}", font=("Helvetica", 14, "bold"))
        self.username_label.pack(padx=(0, 40))

        self.balance_label = ttk.Label(user_info_frame, text=f"Balance: {self.user_info['balance']:.2f}", style="Green.TLabel")
        self.balance_label.pack(padx=(0, 40))

    def update_balance_label(self):
        self.user_info['balance'] = get_balance(self.user_info['id'])
        self.balance_label.config(text=f"Balance: {self.user_info['balance']:.2f}")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
