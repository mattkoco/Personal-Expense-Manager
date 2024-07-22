import json
import tkinter as tk
from tkinter import messagebox, ttk

class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.load_expenses()

    def add_expense(self, description, amount):
        self.expenses.append({"description": description, "amount": amount})
        self.save_expenses()

    def view_expenses(self):
        return self.expenses

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            self.save_expenses()
        else:
            print("Invalid index!")

    def save_expenses(self):
        with open(self.filename, "w") as file:
            json.dump(self.expenses, file)

    def load_expenses(self):
        try:
            with open(self.filename, "r") as file:
                try:
                    self.expenses = json.load(file)
                except json.JSONDecodeError:
                    print("The JSON file is empty or their is a malformed JSON. Starting with an empty list.")
                    self.expenses = []
        except FileNotFoundError:
            print(f"{self.filename} not found. Starting with an empty list.")
            self.expenses = []

    def generate_summary(self):
        total = sum(expense["amount"] for expense in self.expenses)
        return total

    def compare_to_us_average(self):
        us_average_yearly_spending = 63000
        total = self.generate_summary()
        difference = us_average_yearly_spending - total
        percentage = (total / us_average_yearly_spending) * 100
        return total, us_average_yearly_spending, difference, percentage

class ExpenseTrackerApp:
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#43696b", foreground="black")
        style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")

        # Add Expence
        self.frame_add = ttk.LabelFrame(self.root, text="Add Expense", padding=10)
        self.frame_add.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(self.frame_add, text="Description:").grid(row=0, column=0, sticky="w")
        self.description_entry = ttk.Entry(self.frame_add, width=40, foreground="black")
        self.description_entry.grid(row=0, column=1)

        ttk.Label(self.frame_add, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_entry = ttk.Entry(self.frame_add, width=40, foreground="black")
        self.amount_entry.grid(row=1, column=1)

        self.add_button = ttk.Button(self.frame_add, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # View Expenses
        self.frame_view = ttk.LabelFrame(self.root, text="View Expenses", padding=10)
        self.frame_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.view_button = ttk.Button(self.frame_view, text="View Expenses", command=self.view_expenses)
        self.view_button.grid(row=0, column=0, columnspan=2, pady=10)

        self.expense_listbox = tk.Listbox(self.frame_view, width=60, height=10, bg="#ffffff", selectbackground="#4CAF50")
        self.expense_listbox.grid(row=1, column=0, columnspan=2, pady=5)

        # Delete Expense
        self.frame_delete = ttk.LabelFrame(self.root, text="Delete Expense", padding=10)
        self.frame_delete.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(self.frame_delete, text="Expense Index:").grid(row=0, column=0, sticky="w")
        self.index_entry = ttk.Entry(self.frame_delete, width=20, foreground="black")
        self.index_entry.grid(row=0, column=1)

        self.delete_button = ttk.Button(self.frame_delete, text="Delete Expense", command=self.delete_expense)
        self.delete_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Generate Summary
        self.frame_summary = ttk.LabelFrame(self.root, text="Summary", padding=10)
        self.frame_summary.pack(fill="both", expand=True, padx=10, pady=10)

        self.summary_button = ttk.Button(self.frame_summary, text="Generate Summary", command=self.generate_summary)
        self.summary_button.grid(row=0, column=0, columnspan=2, pady=10)

        # Compare to US Avarage
        self.frame_compare = ttk.LabelFrame(self.root, text="Compare to US Average", padding=10)
        self.frame_compare.pack(fill="both", expand=True, padx=10, pady=10)

        self.compare_button = ttk.Button(self.frame_compare, text="Compare to US Average", command=self.compare_to_us_average)
        self.compare_button.grid(row=0, column=0, columnspan=2, pady=10)

        self.comparison_label = tk.Label(self.frame_compare, text="", wraplength=400, justify="left", bg="#f0f0f0")
        self.comparison_label.grid(row=1, column=0, columnspan=2)

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        if description and amount:
            try:
                amount = float(amount)
                self.tracker.add_expense(description, amount)
                messagebox.showinfo("Success", "Expense added successfully!")
                self.description_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
        else:
            messagebox.showerror("Error", "Please enter both description and amount.")

    def view_expenses(self):
        expenses = self.tracker.view_expenses()
        self.expense_listbox.delete(0, tk.END)
        for i, expense in enumerate(expenses):
            self.expense_listbox.insert(tk.END, f"{i + 1}. {expense['description']}: ${expense['amount']:.2f}")

    def delete_expense(self):
        index = self.index_entry.get()
        if index:
            try:
                index = int(index) - 1
                self.tracker.delete_expense(index)
                messagebox.showinfo("Success", "Expense deleted successfully!")
                self.index_entry.delete(0, tk.END)
                self.view_expenses()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid index.")
        else:
            messagebox.showerror("Error", "Please enter an index.")

    def generate_summary(self):
        total = self.tracker.generate_summary()
        messagebox.showinfo("Summary", f"Total Expenses: ${total:.2f}")

    def compare_to_us_average(self):
        total, us_average, difference, percentage = self.tracker.compare_to_us_average()
        comparison = (f"Your total expenses are ${total:.2f}.\n"
                      f"The average yearly spending in the US is ${us_average:.2f}.\n"
                      f"You have spent {percentage:.2f}% of the average yearly spending.\n")
        if total > us_average:
            comparison += f"You have spent ${-difference:.2f} more than the average yearly spending."
        else:
            comparison += f"You have spent ${difference:.2f} less than the average yearly spending."
        self.comparison_label.config(text=comparison)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
