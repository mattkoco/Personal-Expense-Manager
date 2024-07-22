import json

class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.load_expenses()

    def add_expense(self, description, amount):
        self.expenses.append({"description": description, "amount": amount})
        self.save_expenses()

    def view_expenses(self):
        for i, expense in enumerate(self.expenses):
            print(f"{i + 1}. {expense['description']}: ${expense['amount']}")

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
        print(f"Total Expenses: ${total:.2f}")
        return total

    def compare_to_us_average(self):
        us_average_yearly_spending = 63000
        total = self.generate_summary()
        difference = us_average_yearly_spending - total
        percentage = (total / us_average_yearly_spending) * 100
        print(f"Your total expenses are ${total:.2f}.")
        print(f"The average yearly spending in the US is ${us_average_yearly_spending:.2f}.")
        print(f"You have spent {percentage:.2f}% of the average yearly spending.")
        if total > us_average_yearly_spending:
            print(f"You have spent ${-difference:.2f} more than the average yearly spending.")
        else:
            print(f"You have spent ${difference:.2f} less than the average yearly spending.")

if __name__ == "__main__":
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Generate Summary")
        print("5. Compare to US Average")
        print("6. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            tracker.add_expense(description, amount)
        elif choice == "2":
            tracker.view_expenses()
        elif choice == "3":
            index = int(input("Enter expense index to delete: ")) - 1
            tracker.delete_expense(index)
        elif choice == "4":
            tracker.generate_summary()
        elif choice == "5":
            tracker.compare_to_us_average()
        elif choice == "6":
            break
        else:
            print("Invalid choice!")
