import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from features.read_file import read_csv_file
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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