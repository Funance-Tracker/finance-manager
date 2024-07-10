import tkinter as tk
from tkinter import ttk, messagebox
from features.api import fetch_data, convert

class CurrencyConvertPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.data = fetch_data()

        style = ttk.Style()
        style.configure("LimeGreen.TButton", background="#32CD32", foreground="#32CD32")
        style.configure("Form.TLabel", font=("Arial", 14))
        style.configure("Form.TLabelframe.Label", font=("Arial", 18, "bold"))

        # Currency Conversion Form
        convert_frame = ttk.LabelFrame(self, text="Currency Conversion")
        convert_frame.place(x=0, y=0, relwidth=1, relheight=1)

        ttk.Label(convert_frame, text="Amount in JOD:", style="Form.TLabel").place(x=0, y=100)
        self.amount_entry = ttk.Entry(convert_frame)
        self.amount_entry.place(x=250, y=100, width=200, height=24)  # Adjusted x position

        ttk.Label(convert_frame, text="To Currency:", style="Form.TLabel").place(x=0, y=200)
        self.to_currency_var = tk.StringVar(value='USD')  # Set default value to USD
        self.to_currency_dropdown = ttk.Combobox(convert_frame, textvariable=self.to_currency_var, values=list(self.data.keys()))
        self.to_currency_dropdown.place(x=250, y=200, width=200, height=24)  # Adjusted x position

        self.convert_button = ttk.Button(convert_frame, text="Convert", command=self.convert_currency, style="LimeGreen.TButton")
        self.convert_button.place(x=150, y=250, width=150)  # Adjusted x position

        self.result_label = ttk.Label(convert_frame, text="", style="Form.TLabel")
        self.result_label.place(x=20, y=300)  # Adjusted x position

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