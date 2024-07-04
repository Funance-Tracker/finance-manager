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