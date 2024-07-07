import tkinter as tk
from tkinter import messagebox, ttk
from register_sign_in.register import register_user

class RegisterApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="Registration", font=("Helvetica", 24, "bold"), foreground="#333")
        label.pack(pady=10)

        username_label = ttk.Label(self, text="Username:", font=("Helvetica", 12))
        username_label.pack()

        self.username_entry = ttk.Entry(self, width=30, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        email_label = ttk.Label(self, text="Email:", font=("Helvetica", 12))
        email_label.pack()

        self.email_entry = ttk.Entry(self, width=30, font=("Helvetica", 12))
        self.email_entry.pack(pady=5)

        password_label = ttk.Label(self, text="Password:", font=("Helvetica", 12))
        password_label.pack()

        self.password_entry = ttk.Entry(self, show="*", width=30, font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        confirm_password_label = ttk.Label(self, text="Confirm Password:", font=("Helvetica", 12))
        confirm_password_label.pack()

        self.confirm_password_entry = ttk.Entry(self, show="*", width=30, font=("Helvetica", 12))
        self.confirm_password_entry.pack(pady=5)

        register_button = ttk.Button(self, text="Register", command=self.register)
        register_button.pack(pady=10)

        login_label = ttk.Label(self, text="Already have an account?", font=("Helvetica", 10))
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
