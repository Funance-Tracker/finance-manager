# pip install tk
# pip install SpeechRecognition
# pip install PyAudio==0.2.14
# pip install psycopg2
# pip install pyttsx3
# pip install python-dotenv

import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from PostgresDB.postgres_db import PostgresDB

class VoiceCommandApp(tk.Tk):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.title("Voice Command App")

        instructions_text = (
            "Available Commands:\n\n"
            "1. To show your transactions, say 'Show my transactions'.\n"
            "2. To show your balance, say 'Show my balance'.\n"
            "3. To show your debts, say 'Show my debts'.\n"
            "4. To show your information, say 'Show my information'."
        )
        self.instructions_label = tk.Label(self, text=instructions_text, font=("Century", 12), justify="left")
        self.instructions_label.pack(pady=20)

        self.speak_button = tk.Button(self, text="Speak", command=self.process_voice_command, bg="#ADD8E6")
        self.speak_button.pack(pady=20)

        self.result_label = tk.Label(self, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=20)

    def process_voice_command(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                self.result_label.config(text="Listening....")  
                self.update() 
                audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio)
            self.result_label.config(text=f"Command: {command}")

            if "show my transactions" in command.lower():
                self.show_transactions()
            elif "show my balance" in command.lower():
                self.show_balance()
            elif "show my debts" in command.lower():
                self.show_debts()
            elif "show my information" in command.lower():
                self.show_user_info()
            else:
                self.result_label.config(text="Command not recognized.")

        except sr.UnknownValueError:
            self.result_label.config(text="Sorry, I did not understand the command.")
        except sr.RequestError as e:
            self.result_label.config(text=f"Could not request results; {e}")

    def fetch_transactions(self):
        try:
            db = PostgresDB()
            connection = db.get_connection()
            cur = connection.cursor()
            # add here transactions_date column with new schema
            cur.execute("SELECT amount, description FROM transactions WHERE user_id = %s", (self.user_id,))
            transactions = cur.fetchall()
            cur.close()

            return transactions
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []

    def fetch_balance(self):
        try:
            db = PostgresDB()
            connection = db.get_connection()
            cur = connection.cursor()

            cur.execute("SELECT balance FROM users WHERE id = %s", (self.user_id,))
            balance = cur.fetchone()[0]
            cur.close()

            return balance
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0.0

    def fetch_debts(self):
        try:
            db = PostgresDB()
            connection = db.get_connection()
            cur = connection.cursor()
            # add here debts_date column with new schema
            cur.execute("SELECT amount, description FROM debts WHERE user_id = %s", (self.user_id,))
            debts = cur.fetchall()
            cur.close()

            return debts
        except Exception as e:
            print(f"Error fetching debts: {e}")
            return []

    def fetch_user_info(self):
        try:
            db = PostgresDB()
            connection = db.get_connection()
            cur = connection.cursor()

            cur.execute("SELECT username, email, password FROM users WHERE id = %s", (self.user_id,))
            user_info = cur.fetchone()
            cur.close()

            return user_info
        except Exception as e:
            print(f"Error fetching user information: {e}")
            return None

    def show_transactions(self):
        transactions = self.fetch_transactions()
        transactions_text = "\n".join([f"Amount: {amount}, Description: {description}" for amount, description in transactions])
        messagebox.showinfo("Transactions", transactions_text if transactions_text else "No transactions found.")

    def show_balance(self):
        balance = self.fetch_balance()
        messagebox.showinfo("Balance", f"Your balance is: {balance} JD")

    def show_debts(self):
        debts = self.fetch_debts()
        debts_text = "\n".join([f"Amount: {amount}, Description: {description}" for amount, description in debts])
        messagebox.showinfo("Debts", debts_text if debts_text else "No debts found.")

    def show_user_info(self):
        user_info = self.fetch_user_info()
        if user_info:
            username, email, password = user_info
            messagebox.showinfo("User Information", f"Username: {username}\nEmail: {email}")
        else:
            messagebox.showerror("Error", "Failed to fetch user information.")


if __name__ == "__main__":
    user_id = 16  
    app = VoiceCommandApp(user_id)
    app.mainloop()
