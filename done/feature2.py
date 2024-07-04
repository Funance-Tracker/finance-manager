import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from features.read_file import read_csv_file, plot_column_chart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# upload and plot csv file using read_file file
def upload_and_plot():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]) 
    if file_path:
        try:
            data = read_csv_file(file_path)
            display_transaction_summary(data)
            plot_column_chart_in_tkinter(data)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing file: {e}")

# calculate the transactions (summary) for the user
def display_transaction_summary(data):
    total, summary = calculate_transaction_summary(data)

    summary_text = f"Total: {total} JD\n\n"
    for category, amount in summary.items():
        summary_text += f"Category: {category}, Amount: {amount} JD\n"

    summary_label.config(text=summary_text)

def calculate_transaction_summary(data):
    summary = {}
    total = 0.0

    for amount, category in data:
        if category in summary:
            summary[category] += amount
        else:
            summary[category] = amount
        total += amount
    
    return total, summary
# draw a plot
def plot_column_chart_in_tkinter(data):
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


    # tkinter GUI layout 
    canvas = FigureCanvasTkAgg(figure, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

def main():
    global summary_label, plot_frame

    root = tk.Tk()
    root.title("CSV Plot Generator")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    upload_label = ttk.Label(main_frame, text="Upload CSV File:", font=("Helvetica", 15))
    upload_label.grid(row=0, column=9)

    upload_button = ttk.Button(main_frame, text="Upload", command=upload_and_plot, width=20, padding=(10, 10))
    upload_button.grid(row=0, column=10)

    summary_label = ttk.Label(main_frame, text="", padding=10, justify=tk.LEFT , font=("Helvetica", 15))
    summary_label.grid(row=1, column=10, columnspan=2, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    plot_frame = ttk.Frame(main_frame, padding=20)
    plot_frame.grid(row=2, column=10, columnspan=1, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    root.mainloop()

if __name__ == "__main__":
    main()
