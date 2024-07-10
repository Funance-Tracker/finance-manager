import tkinter as tk
from tkinter import messagebox, ttk
from register_sign_in.register import register_user
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL

class RegisterApp(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        container = ttk.Frame(self)
        container.place(x=0, y=0, relwidth=1, relheight=1)

        # Left side for title, logo, and placeholder text
        # Left side for title, logo, and placeholder text
        title_frame = ttk.Frame(container)
        title_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        title_label = ttk.Label(title_frame, text="Finance Manager", font=("Helvetica", 24, "bold"), foreground="#4ECCA3")
        title_label.place(relx=0.5, rely=0.3, anchor="center")

        # Add logo below the title (use your logo image path)
        logo_path = "./logo.png"
        logo_image = Image.open(logo_path)

        # Ensure the image size is not zero or negative
        if title_frame.winfo_width() > 0 and title_frame.winfo_height() > 0:
            target_width = int(title_frame.winfo_width() * 0.3)
            target_height = int(title_frame.winfo_height() * 0.2)
            logo_image = logo_image.resize((250, 150))
        else:
            messagebox.showerror("Error", "Frame dimensions are invalid.")
            return
        
        logo_photo = ImageTk.PhotoImage(logo_image)
        
        logo_label = ttk.Label(title_frame, image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
        logo_label.place(relx=0.5, rely=0.45, anchor="center")

        placeholder_text = (
            "Welcome to the Finance Manager app. \n"
            "Manage your finances Efficiently and Effectively.\n"
            "Login to get started."
        )

        placeholder_label = ttk.Label(title_frame, text=placeholder_text, font=("Helvetica", 18), wraplength=300, justify="center")
        placeholder_label.place(relx=0.5, rely=0.7, anchor="center")

        # Right side for form
        form_frame = ttk.Frame(container)
        form_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        username_label = ttk.Label(form_frame, text="Username", font=("Helvetica", 18))
        username_label.place(relx=0.5, rely=0.2, anchor="center")

        self.username_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 18))
        self.username_entry.place(relx=0.5, rely=0.25, anchor="center")

        email_label = ttk.Label(form_frame, text="Email", font=("Helvetica", 18))
        email_label.place(relx=0.5, rely=0.3, anchor="center")

        self.email_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 18))
        self.email_entry.place(relx=0.5, rely=0.35, anchor="center")

        password_label = ttk.Label(form_frame, text="Password", font=("Helvetica", 18))
        password_label.place(relx=0.5, rely=0.4, anchor="center")

        self.password_entry = ttk.Entry(form_frame, show="*", width=30, font=("Helvetica", 18))
        self.password_entry.place(relx=0.5, rely=0.45, anchor="center")

        confirm_password_label = ttk.Label(form_frame, text="Confirm Password", font=("Helvetica", 18))
        confirm_password_label.place(relx=0.5, rely=0.5, anchor="center")

        self.confirm_password_entry = ttk.Entry(form_frame, show="*", width=30, font=("Helvetica", 18))
        self.confirm_password_entry.place(relx=0.5, rely=0.55, anchor="center")

        style = ttk.Style(self)
        style.configure("Green.TButton", background="#4ECCA3", foreground="#4ECCA3", font=("Helvetica", 18))
        style.configure("Blue.TButton", background="blue", foreground="blue", font=("Helvetica", 18))

        register_button = ttk.Button(form_frame, text="Register", style="Green.TButton", command=self.register)
        register_button.place(relx=0.5, rely=0.65, anchor="center")

        login_label = ttk.Label(form_frame, text="Already have an account?", font=("Helvetica", 16))
        login_label.place(relx=0.5, rely=0.73, anchor="center")

        login_button = ttk.Button(form_frame, text="Login", style="Blue.TButton", command=self.controller.show_login)
        login_button.place(relx=0.5, rely=0.77, anchor="center")

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

        registration_result = register_user(username, email, password)

        if registration_result == "registered_successfully":
            messagebox.showinfo("Success", "Registration successful. You can now login.")
            self.controller.show_login()  # Switch back to login form after registration
        elif registration_result == "not_valid_email":
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email.")
        elif registration_result == "already_exist":
            messagebox.showerror("Error", "User with this email already exists. Please use a different email.")
        else:
            messagebox.showerror("Error", "An error occurred. Please try again later.")
