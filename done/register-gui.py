import tkinter as tk
from tkinter import messagebox, ttk
from register_sign_in.register import register_user  # Adjust the import path accordingly
from PostgresDB.postgres_db import PostgresDB  # Ensure this import is correct
import sign_in_gui  # Import sign_in_gui to render the sign-in page

class RegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")

        # Configure root window to be full screen size and resizable
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(True, True)


        self.db = PostgresDB()
        self.connection = self.db.get_connection()

        # Background frame with glassmorphism effect
        self.bg_frame = tk.Frame(root, bg='#ffffff', bd=0, relief='solid')
        self.bg_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.bg_frame.config(bg='#ffffff', highlightbackground='white', highlightcolor='white', highlightthickness=0, padx="100", pady="100")

        self.title_label = tk.Label(self.bg_frame, text="Register", font=("Helvetica", 40, "bold"), bg="white", fg="#000000")
        self.title_label.pack(pady=30)

        # Username entry
        self.username_label = ttk.Label(self.bg_frame, text="Username:", background='white')
        self.username_label.pack(pady=5)
        style = ttk.Style()
        style.configure('Padded.TEntry', padding=(5, 5))  # Adjust padding values as needed
        self.username_entry = ttk.Entry(self.bg_frame, width=30, font=('Arial', 17), style='Padded.TEntry')
        self.username_entry.pack(pady=5)

        # Email entry
        self.email_label = ttk.Label(self.bg_frame, text="Email:", background='white')
        self.email_label.pack(pady=5)
        self.email_entry = ttk.Entry(self.bg_frame, width=30, font=('Arial', 17), style='Padded.TEntry')  # Adjusted font size
        self.email_entry.pack(pady=5)

        # Password entry
        self.password_label = ttk.Label(self.bg_frame, text="Password:", background='white')
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.bg_frame, show="*", width=30, font=('Arial', 17), style='Padded.TEntry')  # Adjusted font size
        self.password_entry.pack(pady=5)

        # Confirm Password entry
        self.confirm_password_label = ttk.Label(self.bg_frame, text="Confirm Password:", background='white')
        self.confirm_password_label.pack(pady=5)
        self.confirm_password_entry = ttk.Entry(self.bg_frame, show="*", width=30, font=('Arial', 17), style='Padded.TEntry')  # Adjusted font size
        self.confirm_password_entry.pack(pady=5)


        # Register button
        self.register_button = tk.Button(self.bg_frame, text="Register", command=self.register, font=('Arial', 12), bg='#4267B2', fg='white', relief='flat')
        self.register_button.pack(pady=20, ipadx=10, ipady=5)

        # Copyright text
        self.copyright_label = tk.Label(self.bg_frame, text="© 2024", font=('Arial', 10), bg="white", fg="#999999")
        self.copyright_label.pack(side='bottom', pady=10)

        # Set focus to username entry on startup
        self.username_entry.focus()

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            return

        result = register_user(username, email, password)

        if result == "not_valid_email":
            messagebox.showerror("Error", "Please enter a valid email format.")
            return
        elif result == "already_exist":
            messagebox.showerror("Error", "User with this email already exists.")
            return
        elif result == "done":
            messagebox.showinfo("Success", "Registration successful. Please sign in.")
            self.render_sign_in_page()
            return
        else:
            messagebox.showerror("Error", "Registration failed. Please try again.")

    def render_sign_in_page(self):
        self.root.destroy()
        sign_in_gui.main()

def main():
    root = tk.Tk()
    app = RegisterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()