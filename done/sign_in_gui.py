import tkinter as tk
from tkinter import messagebox, ttk
from register_sign_in.sign_in import sign_in, validate_email  # Adjust the import path accordingly
from PostgresDB.postgres_db import PostgresDB  # Ensure this import is correct

class SignInApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign In")

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
        self.bg_frame.config(bg='#ffffff', highlightbackground='white', highlightcolor='white', highlightthickness=0, padx=50, pady=50)

        self.title_label = tk.Label(self.bg_frame, text="Sign-In", font=("Helvetica", 40, "bold"), bg="white", fg="#000000")
        self.title_label.pack(pady=30)

        # Email entry
        self.email_label = ttk.Label(self.bg_frame, text="Email:", background='white')
        self.email_label.pack(pady=5)
        style = ttk.Style()
        style.configure('Padded.TEntry', padding=(5, 5))  # Adjust padding values as needed
        self.email_entry = ttk.Entry(self.bg_frame, width=30, font=('Arial', 17), style='Padded.TEntry')  # Adjusted font size and padding
        self.email_entry.pack(pady=5)

        # Password entry
        self.password_label = ttk.Label(self.bg_frame, text="Password:", background='white')
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.bg_frame, show="*", width=30, font=('Arial', 17), style='Padded.TEntry')  # Adjusted font size and padding
        self.password_entry.pack(pady=5)


        # Sign In button
        self.sign_in_button = tk.Button(self.bg_frame, text="Sign In", command=self.sign_in, font=('Arial', 12), bg='#4267B2', fg='white', relief='flat')
        self.sign_in_button.pack(pady=20, ipadx=10, ipady=5)

        # Copyright text
        self.copyright_label = tk.Label(self.bg_frame, text="© 2024", font=('Arial', 10), bg="white", fg="#999999")
        self.copyright_label.pack(side='bottom', pady=10)

        # Set focus to email entry on startup
        self.email_entry.focus()

    def sign_in(self):
        
        email = self.email_entry.get()
        password = self.password_entry.get()

        user_data = sign_in(email, password)
        # messagebox.showerror(f"Email: {email}, Password: {password}")

        if user_data == "not_valid_email":
            messagebox.showerror("Error", "Please enter a valid email format.")
            return
        elif user_data == "not_exist":
            messagebox.showerror("Error", f"User with email '{email}' does not exist.")
            self.password_entry.delete(0, tk.END)
            return
        elif user_data == "wrong_password":
            messagebox.showerror("Error", "Incorrect password. Please try again.")
            self.password_entry.delete(0, tk.END)
            return
        elif isinstance(user_data, dict):
            messagebox.showinfo("Success", f"Welcome, {user_data['username']}!")
            self.render_home_page()
            return
        else:
            messagebox.showerror("Error", str(user_data))



    def render_home_page(self):
        # Assuming you will work on the home page rendering later
        self.root.destroy()
        import home_page  # Make sure home_page.py is in the same directory or adjust the import path accordingly
        home_page.main()

def main():
    root = tk.Tk()
    app = SignInApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
