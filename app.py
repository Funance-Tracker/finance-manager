import tkinter as tk
from tkinter import ttk
from GUI.login import LoginApp
from GUI.register import RegisterApp

class FinanceManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Finance Manager")

        # Center window on screen and set size
        window_width = 1250
        window_height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Introduction text (centered)
        introduction_label = ttk.Label(main_frame, text="Welcome to Finance Manager!", font=("Arial", 24))
        introduction_label.pack(pady=50)

        # Container for login/register forms
        form_container = ttk.Frame(main_frame)
        form_container.pack(pady=20)

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