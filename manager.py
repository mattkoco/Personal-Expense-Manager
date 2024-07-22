class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, description, amount):
        self.expenses.append({"description": description, "amount": amount})

    def view_expenses(self):
        for i, expense in enumerate(self.expenses):
            print(f"{i + 1}. {expense['description']}: ${expense['amount']}")

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
        else:
            print("Invalid index!")

if __name__ == "__main__":
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Quit")
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
            break
        else:
            print("Invalid choice!")
