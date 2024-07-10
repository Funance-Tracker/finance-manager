import tkinter as tk
from tkinter import ttk
from GUI.login import LoginApp
from GUI.register import RegisterApp

class FinanceManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Finance Manager")

        # Maximize the window and keep the title bar and exit button visible
        self.state('zoomed')

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Initially show the login form
        self.show_login()

    def show_login(self):
        # Destroy current frame if it exists
        if hasattr(self, "current_frame"):
            self.current_frame.destroy()

        # Create and display login form
        self.current_frame = LoginApp(self.main_frame, self)
        self.current_frame.pack(fill="both", expand=True)

    def show_register(self):
        # Destroy current frame if it exists
        if hasattr(self, "current_frame"):
            self.current_frame.destroy()

        # Create and display register form
        self.current_frame = RegisterApp(self.main_frame, self)
        self.current_frame.pack(fill="both", expand=True)

def main():
    app = FinanceManagerApp()
    app.mainloop()

if __name__ == "__main__":
    main()
