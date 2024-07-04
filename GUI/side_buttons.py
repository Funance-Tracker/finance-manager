import tkinter as tk
from tkinter import ttk

class SideButtons(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create "Report" button
        report_button = ttk.Button(self, text="Report")
        report_button.pack(fill="x", padx=10, pady=5)

        # Create "Show Debts" button
        show_debts_button = ttk.Button(self, text="Show Debts", command=self.controller.show_debts_frame)
        show_debts_button.pack(fill="x", padx=10, pady=5)
