import json
import tkinter as tk
from tkinter import messagebox

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
                    print("File is empty or malformed JSON. Starting with an empty list.")
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

        self.create_widgets()

    def create_widgets(self):
        # Add Expense
        self.description_label = tk.Label(self.root, text="Description:")
        self.description_label.grid(row=0, column=0)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=0, column=1)

        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=1, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=2, column=0, columnspan=2)

        # View Expenses
        self.view_button = tk.Button(self.root, text="View Expenses", command=self.view_expenses)
        self.view_button.grid(row=3, column=0, columnspan=2)

        # Delete Expense
        self.index_label = tk.Label(self.root, text="Expense Index:")
        self.index_label.grid(row=4, column=0)
        self.index_entry = tk.Entry(self.root)
        self.index_entry.grid(row=4, column=1)

        self.delete_button = tk.Button(self.root, text="Delete Expense", command=self.delete_expense)
        self.delete_button.grid(row=5, column=0, columnspan=2)

        # Generate Summary
        self.summary_button = tk.Button(self.root, text="Generate Summary", command=self.generate_summary)
        self.summary_button.grid(row=6, column=0, columnspan=2)

        # Compare to US Average
        self.compare_button = tk.Button(self.root, text="Compare to US Average", command=self.compare_to_us_average)
        self.compare_button.grid(row=7, column=0, columnspan=2)

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        if description and amount:
            try:
                amount = float(amount)
                self.tracker.add_expense(description, amount)
                messagebox.showinfo("Success", "Expense added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
        else:
            messagebox.showerror("Error", "Please enter both description and amount.")

    def view_expenses(self):
        expenses = self.tracker.view_expenses()
        expense_list = "\n".join([f"{i + 1}. {expense['description']}: ${expense['amount']}" for i, expense in enumerate(expenses)])
        messagebox.showinfo("Expenses", expense_list if expense_list else "No expenses recorded.")

    def delete_expense(self):
        index = self.index_entry.get()
        if index:
            try:
                index = int(index) - 1
                self.tracker.delete_expense(index)
                messagebox.showinfo("Success", "Expense deleted successfully!")
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
        messagebox.showinfo("Comparison", comparison)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
