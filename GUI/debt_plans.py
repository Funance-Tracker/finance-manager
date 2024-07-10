import tkinter as tk
from tkinter import ttk, messagebox
from model_transaction.balance import get_balance
from model_transaction.transaction import add_new_transaction
from PostgresDB.postgres_db import PostgresDB
from model_transaction.debt import get_debts as gd

class DebtsPlanPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_info = self.controller.user_info

        # Debts Plans Label
        label = ttk.Label(self, text="Debts Plans")
        label.pack(pady=10, padx=10)

        # Frame for Debts Table
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Debts Table
        self.tree = ttk.Treeview(self.table_frame, columns=("amount", "description"), show="headings")
        self.tree.heading("amount", text="Amount", anchor=tk.CENTER, command=lambda: self.sort_column(self.tree, "amount", False))
        self.tree.heading("description", text="Description", anchor=tk.CENTER)
        self.tree.column("amount", width=100, anchor=tk.CENTER)
        self.tree.column("description", width=300, anchor=tk.CENTER)
        self.tree.pack(fill="both", expand=True)

        # Styling the header
        self.tree["style"] = "mystyle.Treeview"
        style = ttk.Style()
        style.configure("mystyle.Treeview.Heading", font=("Arial", 12, "bold"))

        # Generate initial debts table
        self.populate_debts_table()

        # Amount Entry Frame
        amount_frame = ttk.LabelFrame(self, text="Payment Amount")
        amount_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(amount_frame, text="Amount you are willing to pay:").pack(side="left", padx=5, pady=5)
        self.amount_entry = ttk.Entry(amount_frame)
        self.amount_entry.pack(side="left", padx=5, pady=5)

        self.generate_button = ttk.Button(amount_frame, text="Generate Plans", command=self.generate_plans)
        self.generate_button.pack(side="left", padx=5, pady=5)

        # Frame for Generated Plans
        self.plans_frame = ttk.Frame(self)
        
        # Refresh Button
        self.refresh_button = ttk.Button(amount_frame, text="Refresh", command=self.refresh_page)
        self.refresh_button.pack(side="left", padx=5, pady=5)

    def populate_debts_table(self):
        # Clear existing items in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        user_id = self.user_info['id']
        debts = self.get_debts(user_id)
        
        if not debts:
            ttk.Label(self.tree, text="You have no debts to pay off.").pack()
        else:
            for debt in debts:
                self.tree.insert("", "end", values=(debt[0], debt[1]))

    def generate_plans(self):
        try:
            amount = float(self.amount_entry.get())
            user_id = self.user_info['id']
            balance = get_balance(user_id)
            
            if amount > balance:
                messagebox.showerror("Error", "The amount exceeds your available balance.")
                return
            
            # Clear previous results (remove plans frame content)
            for widget in self.plans_frame.winfo_children():
                widget.destroy()

            # Generate plans and display them
            self.generate_plans_based_on_amount(amount)
            
            # Show plans frame
            self.plans_frame.pack(fill="both", expand=True, padx=10, pady=10)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def generate_plans_based_on_amount(self, amount):
        user_id = self.user_info['id']
        debts = self.get_debts(user_id)
        if not debts:
            ttk.Label(self.plans_frame, text="You have no debts to pay off.").pack()
            return

        # Generate payment plans
        plans = self.create_payment_plans(debts, amount)
        if not plans:
            ttk.Label(self.plans_frame, text="The amount is insufficient to create a payment plan.").pack()
        else:
            for plan in plans:
                total_plan_amount = sum(amt for amt, desc in plan)

                if total_plan_amount <= amount:
                    plan_frame = ttk.Frame(self.plans_frame)
                    plan_frame.pack(fill="x", padx=5, pady=5)

                    plan_text = ", ".join([f"{amt} ({desc})" for amt, desc in plan])
                    plan_label = ttk.Label(plan_frame, text=plan_text)
                    plan_label.pack(side="left", padx=5, pady=5)

                    pay_button = ttk.Button(plan_frame, text="Pay this plan", command=lambda p=plan: self.pay_plan(p, plan_frame))
                    pay_button.pack(side="right", padx=5, pady=5)
                else:
                    # Skip displaying plans that exceed the entered amount
                    continue

    def create_payment_plans(self, debts, amount):
        plans = []
        current_plan = []
        remaining_amount = amount

        for debt in debts:
            if debt[0] <= remaining_amount:
                current_plan.append(debt)
                remaining_amount -= debt[0]
            else:
                if current_plan:
                    plans.append(current_plan)
                current_plan = [debt]
                remaining_amount = amount - debt[0]
        
        if current_plan:
            plans.append(current_plan)

        return plans

    def pay_plan(self, plan, plan_frame):
        user_id = self.user_info['id']
        for amount, description in plan:
            success = add_new_transaction(user_id, amount, f"Paid debt: {description}")
            if success:
                self.delete_debt(user_id, description)
        
        # Remove the plan frame from GUI
        plan_frame.destroy()
        
        messagebox.showinfo("Success", "Debts paid successfully.")
        self.controller.update_balance_label()

    def get_debts(self, user_id):
        db = PostgresDB()
        connection = db.get_connection()
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT amount, description FROM debts WHERE user_id = %s;", (user_id,))
            debts = cursor.fetchall()
            return debts

        except Exception as e:
            print(f"Error retrieving debts: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                db.close()

    def delete_debt(self, user_id, description):
        db = PostgresDB()
        connection = db.get_connection()
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM debts WHERE user_id = %s AND description = %s;", (user_id, description))
            connection.commit()
        
        except Exception as e:
            print(f"Error deleting debt: {e}")
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                db.close()

    def refresh_page(self):
        # Re-create the debts table view
        self.populate_debts_table()

        # Hide plans frame
        self.plans_frame.pack_forget()

    def sort_column(self, tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
