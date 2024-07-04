import csv
import matplotlib.pyplot as plt

def read_csv_file(file_path):
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

def plot_column_chart(data):
    """
    Plots a column chart using the provided data.

    Args:
        data (list of tuple): A list of tuples where each tuple contains a float (amount) and a string (category).
    """
    if not data:
        print("No data to plot.")
        return
    
    amounts, categories = zip(*data)
    
    plt.figure(figsize=(10, 6))
    plt.bar(categories, amounts, color='skyblue')
    
    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.title('Amount by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.show()
