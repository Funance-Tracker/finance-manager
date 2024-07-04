import tkinter as tk
from tkinter import ttk, messagebox
from features.api import fetch_data, convert

# Fetch currency data
data = fetch_data()

# Tkinter GUI
def convert_currency():
    try:
        amount = float(amount_entry.get())
        to_currency = to_currency_var.get()
        from_currency = 'JOD'  # Fixed 'JOD' as the source currency
        converted_amount = convert(amount, from_currency, to_currency, data)
        if converted_amount is not None:
            result_label.config(text=f"{amount:.2f} {from_currency} is equivalent to {converted_amount:.2f} {to_currency}")
        else:
            messagebox.showerror("Conversion Error", f"Conversion failed for {from_currency} to {to_currency}.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount.")

# Create main window
root = tk.Tk()
root.title("Currency Converter")
root.state('zoomed')  # Maximize the window

# Center frame near the top middle of the screen
center_frame = tk.Frame(root)
center_frame.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

# Widgets for center frame
amount_label = tk.Label(center_frame, text="Amount in JOD:")
amount_entry = tk.Entry(center_frame)
to_currency_label = tk.Label(center_frame, text="To Currency:")
to_currency_var = tk.StringVar(value='USD')  # Set default value to USD
to_currency_dropdown = ttk.Combobox(center_frame, textvariable=to_currency_var, values=list(data.keys()))
convert_button = tk.Button(center_frame, text="Convert", command=convert_currency)
result_label = tk.Label(center_frame, text="")

# Layout widgets for center frame
amount_label.grid(row=0, column=0, padx=10, pady=10)
amount_entry.grid(row=0, column=1, padx=10, pady=10)
to_currency_label.grid(row=1, column=0, padx=10, pady=10)
to_currency_dropdown.grid(row=1, column=1, padx=10, pady=10)
convert_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the main event loop
root.mainloop()
