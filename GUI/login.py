import tkinter as tk
from tkinter import messagebox, ttk
from register_sign_in.sign_in import sign_in
from GUI.main import Home

class LoginApp(ttk.Frame):
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

        email_label = ttk.Label(form_frame, text="Email:", font=("Helvetica", 12))
        email_label.pack(pady=(10, 5))

        self.email_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.email_entry.pack(pady=(5, 10))

        password_label = ttk.Label(form_frame, text="Password:", font=("Helvetica", 12))
        password_label.pack(pady=(10, 5))

        self.password_entry = ttk.Entry(form_frame, show="*", width=30, font=("Helvetica", 12))
        self.password_entry.pack(pady=(5, 10))

        login_button = ttk.Button(form_frame, text="Login", command=self.login)
        login_button.pack(pady=(10, 10))

        register_label = ttk.Label(form_frame, text="Don't have an account?", font=("Helvetica", 10))
        register_label.pack(pady=(10, 5))

        register_button = ttk.Button(form_frame, text="Register", command=self.parent.show_register)
        register_button.pack(pady=(5, 10))

        # Center the form frame content
        form_frame.pack_propagate(False)
        form_frame.configure(width=600, height=540)

        # Center the content in the form frame
        form_frame.pack(side="right", fill="both", expand=True)
        for widget in form_frame.winfo_children():
            widget.pack(anchor="center", pady=(10, 5))

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
