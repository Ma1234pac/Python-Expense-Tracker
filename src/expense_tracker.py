import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Optional

import matplotlib.pyplot as plt


class ExpenseTracker:
    """Manage personal expenses using a CSV file."""

    FIELDNAMES = ["id", "date", "category", "description", "amount"]

    def __init__(self, file_path: str = "data/expenses.csv"):
        self.file_path = Path(file_path)
        self.expenses: List[Dict] = []
        self._load_expenses()

    def _load_expenses(self) -> None:
        """Load expenses from the CSV file."""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_expenses()
            return

        try:
            with self.file_path.open(
                "r",
                encoding="utf-8",
                newline=""
            ) as file:
                reader = csv.DictReader(file)

                self.expenses = []

                for row in reader:
                    self.expenses.append({
                        "id": int(row["id"]),
                        "date": row["date"],
                        "category": row["category"],
                        "description": row["description"],
                        "amount": float(row["amount"])
                    })

        except (OSError, ValueError, KeyError):
            self.expenses = []

    def _save_expenses(self) -> None:
        """Save expenses to the CSV file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open(
            "w",
            encoding="utf-8",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.FIELDNAMES
            )

            writer.writeheader()
            writer.writerows(self.expenses)

    def add_expense(
        self,
        date: str,
        category: str,
        description: str,
        amount: float
    ) -> Dict:
        """Add a new expense."""

        # Validate date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Date must have the format YYYY-MM-DD."
            )

        category = category.strip()
        description = description.strip()

        if not category:
            raise ValueError("Category cannot be empty.")

        if not description:
            raise ValueError("Description cannot be empty.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        new_id = max(
            (expense["id"] for expense in self.expenses),
            default=0
        ) + 1

        expense = {
            "id": new_id,
            "date": date,
            "category": category,
            "description": description,
            "amount": round(float(amount), 2)
        }

        self.expenses.append(expense)
        self._save_expenses()

        return expense

    def get_expenses(
        self,
        category: Optional[str] = None
    ) -> List[Dict]:
        """Return all expenses or filter by category."""

        if category is None:
            return self.expenses.copy()

        return [
            expense
            for expense in self.expenses
            if expense["category"].lower() == category.lower()
        ]

    def get_total(self) -> float:
        """Return the total amount spent."""
        return round(
            sum(expense["amount"] for expense in self.expenses),
            2
        )

    def get_average(self) -> float:
        """Return the average expense."""
        if not self.expenses:
            return 0.0

        return round(
            self.get_total() / len(self.expenses),
            2
        )

    def get_total_by_category(self) -> Dict[str, float]:
        """Return total spending grouped by category."""

        totals = defaultdict(float)

        for expense in self.expenses:
            totals[expense["category"]] += expense["amount"]

        return {
            category: round(amount, 2)
            for category, amount in totals.items()
        }

    def get_largest_expense(self) -> Optional[Dict]:
        """Return the largest expense."""

        if not self.expenses:
            return None

        return max(
            self.expenses,
            key=lambda expense: expense["amount"]
        )

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense by ID."""

        for expense in self.expenses:
            if expense["id"] == expense_id:
                self.expenses.remove(expense)
                self._save_expenses()
                return True

        return False

    def create_category_chart(
        self,
        output_path: str = "reports/expenses_by_category.png"
    ) -> None:
        """Create a pie chart showing expenses by category."""

        totals = self.get_total_by_category()

        if not totals:
            raise ValueError(
                "There are no expenses to display."
            )

        output_file = Path(output_path)
        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        labels = list(totals.keys())
        values = list(totals.values())

        plt.figure(figsize=(8, 8))

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Expenses by Category")

        plt.tight_layout()

        plt.savefig(output_file)

        plt.close()


def display_expenses(expenses: List[Dict]) -> None:
    """Display expenses in a readable table."""

    if not expenses:
        print("\nNo expenses found.\n")
        return

    print("\nExpenses")
    print("-" * 75)

    print(
        f"{'ID':<5}"
        f"{'Date':<12}"
        f"{'Category':<15}"
        f"{'Description':<25}"
        f"{'Amount':>10}"
    )

    print("-" * 75)

    for expense in expenses:
        print(
            f"{expense['id']:<5}"
            f"{expense['date']:<12}"
            f"{expense['category']:<15}"
            f"{expense['description']:<25}"
            f"€{expense['amount']:>9.2f}"
        )

    print()


def display_summary(manager: ExpenseTracker) -> None:
    """Display expense statistics."""

    print("\n===== EXPENSE SUMMARY =====")

    print(f"Total expenses: €{manager.get_total():.2f}")
    print(f"Average expense: €{manager.get_average():.2f}")

    largest = manager.get_largest_expense()

    if largest:
        print(
            f"Largest expense: "
            f"€{largest['amount']:.2f} "
            f"({largest['description']})"
        )

    print("\nExpenses by category:")

    category_totals = manager.get_total_by_category()

    for category, amount in category_totals.items():
        print(f"  {category}: €{amount:.2f}")

    print("============================\n")


def print_menu() -> None:
    """Display the main menu."""

    print("\n===== EXPENSE TRACKER =====")
    print("1. Add expense")
    print("2. Show all expenses")
    print("3. Filter by category")
    print("4. Show summary")
    print("5. Delete expense")
    print("6. Create category chart")
    print("7. Exit")
    print("===========================")


def main() -> None:
    """Run the command-line application."""

    manager = ExpenseTracker()

    while True:

        print_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":

            date = input(
                "Enter date (YYYY-MM-DD): "
            ).strip()

            category = input(
                "Enter category: "
            ).strip()

            description = input(
                "Enter description: "
            ).strip()

            try:
                amount = float(
                    input("Enter amount (€): ")
                )

                expense = manager.add_expense(
                    date,
                    category,
                    description,
                    amount
                )

                print(
                    f"Expense added successfully "
                    f"with ID #{expense['id']}."
                )

            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "2":

            display_expenses(
                manager.get_expenses()
            )

        elif choice == "3":

            category = input(
                "Enter category: "
            ).strip()

            display_expenses(
                manager.get_expenses(category)
            )

        elif choice == "4":

            display_summary(manager)

        elif choice == "5":

            try:
                expense_id = int(
                    input("Enter expense ID: ")
                )

                if manager.delete_expense(expense_id):
                    print("Expense deleted successfully.")
                else:
                    print("Expense not found.")

            except ValueError:
                print("Please enter a valid ID.")

        elif choice == "6":

            try:
                output = "reports/expenses_by_category.png"

                manager.create_category_chart(output)

                print(
                    f"Chart created successfully: {output}"
                )

            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "7":

            print("Goodbye!")
            break

        else:

            print(
                "Invalid option. Please choose "
                "a number between 1 and 7."
            )


if __name__ == "__main__":
    main()
