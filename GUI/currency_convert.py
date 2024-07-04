import tkinter as tk
from tkinter import ttk, messagebox
from features.api import fetch_data, convert


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