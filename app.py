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

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Container for login/register forms
        form_container = ttk.Frame(main_frame)
        form_container.pack(fill="both", expand=True)

        # Initially show the login form
        self.show_login()

    def show_login(self):
        # Destroy current frame if exists
        if hasattr(self, "current_frame"):
            self.current_frame.destroy()

        # Create login form
        self.current_frame = LoginApp(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_register(self):
        # Destroy current frame if exists
        if hasattr(self, "current_frame"):
            self.current_frame.destroy()

        # Create register form
        self.current_frame = RegisterApp(self)
        self.current_frame.pack(fill="both", expand=True)


def main():
    app = FinanceManagerApp()
    app.mainloop()

if __name__ == "__main__":
    main()
