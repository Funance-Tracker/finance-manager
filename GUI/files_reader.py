import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FilesReaderPage(tk.Tk):
    def __init__(self, user_id):
        super().__init__()

        self.title("Files Reader")
        
        # Center window on screen and set size
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.user_id = user_id
        self.transactions = []
        
        self.create_widgets()

    def create_widgets(self):
        # File Reader Frame
        file_reader_frame = ttk.LabelFrame(self, text="Upload and Plot CSV File")
        file_reader_frame.pack(fill="x", padx=10, pady=10)

        self.upload_button = ttk.Button(file_reader_frame, text="Upload CSV", command=self.upload_and_process)
        self.upload_button.pack(side="left", padx=5, pady=5)

        # Text widget to display CSV content
        self.csv_text = tk.Text(self, wrap=tk.WORD, height=15)
        self.csv_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Plot Frame for Matplotlib chart
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def upload_and_process(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                data = self.read_csv_file(file_path)
                self.display_csv_content(data)
                self.plot_column_chart(data)
            except Exception as e:
                messagebox.showerror("Error", f"Error processing file: {e}")

    def read_csv_file(self, file_path):
        """
        Reads a CSV file and extracts rows with two columns.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            list of tuple: A list of tuples where each tuple contains a float (amount) and a string (category).
        """
        data = []
        try:
            with open(file_path, newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    if len(row) == 2:
                        try:
                            amount = float(row[0])
                            category = row[1]
                            data.append((amount, category))
                        except ValueError:
                            print(f"Skipping row with invalid data: {row}")
        except FileNotFoundError:
            print(f"File not found at: {file_path}")
        
        return data

    def display_csv_content(self, data):
        """
        Displays CSV content in a text widget.

        Args:
            data (list of tuple): A list of tuples where each tuple contains a float (amount) and a string (category).
        """
        self.csv_text.delete("1.0", tk.END)  # Clear previous content

        for amount, category in data:
            self.csv_text.insert(tk.END, f"Amount: {amount:.2f}, Category: {category}\n")

    def plot_column_chart(self, data):
        """
        Plots a column chart using the provided data.

        Args:
            data (list of tuple): A list of tuples where each tuple contains a float (amount) and a string (category).
        """
        if not data:
            messagebox.showwarning("No Data", "No data to plot.")
            return

        figure = plt.Figure(figsize=(8, 6))
        ax = figure.add_subplot(111)

        amounts, categories = zip(*data)
        ax.bar(categories, amounts, color='skyblue')
        ax.set_xlabel('Categories')
        ax.set_ylabel('Amount')
        ax.set_title('Amount by Category')
        ax.tick_params(axis='x', rotation=45)
        figure.tight_layout()

        # Clear previous plot in plot_frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Embed Matplotlib plot in Tkinter
        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

