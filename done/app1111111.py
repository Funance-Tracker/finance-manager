import tkinter as tk
from tkinter import messagebox, ttk
from register_sign_in.sign_in import sign_in
from register_sign_in.register import register_user
from GUI.home import Home

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

class LoginApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="Login", font=("Arial", 24))
        label.pack(pady=10)

        email_label = ttk.Label(self, text="Email:")
        email_label.pack()

        self.email_entry = ttk.Entry(self, width=30)
        self.email_entry.pack(pady=5)

        password_label = ttk.Label(self, text="Password:")
        password_label.pack()

        self.password_entry = ttk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=5)

        login_button = ttk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=10)

        register_label = ttk.Label(self, text="Don't have an account?")
        register_label.pack()

        register_button = ttk.Button(self, text="Register", command=self.parent.show_register)
        register_button.pack(pady=5)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Example function (replace with your sign_in function)
        login_result = sign_in(email, password)

        if isinstance(login_result, dict):  # Successful login
            messagebox.showinfo("Success", f"Welcome, {login_result['username']}!")

            # Create Home instance with user_id and start mainloop
            self.parent.destroy()
            home_page = Home(login_result)
            home_page.mainloop()
            print(home_page.user_info)
            

        elif login_result == "not_valid_email":
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email.")
        elif login_result == "not_exist":
            messagebox.showerror("Error", "User does not exist. Please register.")
        elif login_result == "wrong_password":
            messagebox.showerror("Error", "Incorrect password. Please try again.")
        else:
            messagebox.showerror("Error", "An error occurred. Please try again later.")

class RegisterApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="Registration", font=("Arial", 24))
        label.pack(pady=10)

        username_label = ttk.Label(self, text="Username:")
        username_label.pack()

        self.username_entry = ttk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        email_label = ttk.Label(self, text="Email:")
        email_label.pack()

        self.email_entry = ttk.Entry(self, width=30)
        self.email_entry.pack(pady=5)

        password_label = ttk.Label(self, text="Password:")
        password_label.pack()

        self.password_entry = ttk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=5)

        confirm_password_label = ttk.Label(self, text="Confirm Password:")
        confirm_password_label.pack()

        self.confirm_password_entry = ttk.Entry(self, show="*", width=30)
        self.confirm_password_entry.pack(pady=5)

        register_button = ttk.Button(self, text="Register", command=self.register)
        register_button.pack(pady=10)

        login_label = ttk.Label(self, text="Already have an account?")
        login_label.pack()

        login_button = ttk.Button(self, text="Login", command=self.parent.show_login)
        login_button.pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Example function (replace with your register_user function)
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            return

        registration_result = register_user(username, email, password)

        if registration_result == "registered_successfully":
            messagebox.showinfo("Success", "Registration successful. You can now login.")
            self.parent.show_login()  # Switch back to login form after registration
        elif registration_result == "not_valid_email":
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email.")
        elif registration_result == "already_exist":
            messagebox.showerror("Error", "User with this email already exists. Please use a different email.")
        else:
            messagebox.showerror("Error", "An error occurred. Please try again later.")

def main():
    app = FinanceManagerApp()
    app.mainloop()

if __name__ == "__main__":
    main()
