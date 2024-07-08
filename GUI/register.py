import tkinter as tk
from tkinter import messagebox, ttk
from register_sign_in.register import register_user

class RegisterApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Left side for title and placeholder text
        title_frame = ttk.Frame(container)
        title_frame.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)

        title_label = ttk.Label(title_frame, text="Finance Manager", font=("Helvetica", 24, "bold"), foreground="#333")
        title_label.pack(pady=10)

        placeholder_text = (
            "\t        Welcome to the Finance Manager app. \n\n"
            "\t        Manage your finances efficiently and effectively. \n\n"
            "\t        Login to get started."
        )

        placeholder_label = ttk.Label(title_frame, text=placeholder_text, font=("Helvetica", 12), wraplength=500)
        placeholder_label.pack(pady=10)

        # Center the title frame content
        title_frame.pack_propagate(False)
        title_frame.configure(width=320, height=540)

        # Center the content in the title frame
        title_frame.pack(side="left", fill="both", expand=True)
        for widget in title_frame.winfo_children():
            widget.pack(anchor="center", pady=(10, 5))

        # Right side for form
        form_frame = ttk.Frame(container)
        form_frame.pack(side="right", fill="both", expand=True, padx=20)

        username_label = ttk.Label(form_frame, text="Username:", font=("Helvetica", 12))
        username_label.pack(pady=(10, 5))

        self.username_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.username_entry.pack(pady=(5, 10))

        email_label = ttk.Label(form_frame, text="Email:", font=("Helvetica", 12))
        email_label.pack(pady=(10, 5))

        self.email_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.email_entry.pack(pady=(5, 10))

        password_label = ttk.Label(form_frame, text="Password:", font=("Helvetica", 12))
        password_label.pack(pady=(10, 5))

        self.password_entry = ttk.Entry(form_frame, show="*", width=30, font=("Helvetica", 12))
        self.password_entry.pack(pady=(5, 10))

        confirm_password_label = ttk.Label(form_frame, text="Confirm Password:", font=("Helvetica", 12))
        confirm_password_label.pack(pady=(10, 5))

        self.confirm_password_entry = ttk.Entry(form_frame, show="*", width=30, font=("Helvetica", 12))
        self.confirm_password_entry.pack(pady=(5, 10))

        register_button = ttk.Button(form_frame, text="Register", command=self.register)
        register_button.pack(pady=(10, 10))

        login_label = ttk.Label(form_frame, text="Already have an account?", font=("Helvetica", 10))
        login_label.pack(pady=(10, 5))

        login_button = ttk.Button(form_frame, text="Login", command=self.parent.show_login)
        login_button.pack(pady=(5, 10))

        # Center the form frame content
        form_frame.pack_propagate(False)
        form_frame.configure(width=600, height=540)

        # Center the content in the form frame
        form_frame.pack(side="right", fill="both", expand=True)
        for widget in form_frame.winfo_children():
            widget.pack(anchor="center", pady=(10, 5))

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
