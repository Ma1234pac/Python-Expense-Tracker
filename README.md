# 💰 Python Expense Tracker

A simple command-line expense tracker built with Python.

The application allows users to record and manage personal expenses, calculate spending statistics, filter expenses by category, and generate a visual report.

Expense data is stored locally in a CSV file.

## ✨ Features

* Add expenses
* View all expenses
* Filter expenses by category
* Calculate total spending
* Calculate average expense
* Find the largest expense
* Calculate spending by category
* Delete expenses
* Store data in CSV format
* Generate a category-based pie chart
* Automated tests with pytest

## 🛠️ Technologies

* Python 3
* CSV
* pathlib
* datetime
* Matplotlib
* Pytest

## 📁 Project Structure

```text
python-expense-tracker/
│
├── src/
│   ├── __init__.py
│   └── expense_tracker.py
│
├── tests/
│   ├── __init__.py
│   └── test_expense_tracker.py
│
├── data/
│   └── expenses.csv
│
├── reports/
│   └── .gitkeep
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/python-expense-tracker.git
```

Move into the project directory:

```bash
cd python-expense-tracker
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Run:

```bash
python src/expense_tracker.py
```

The application will display:

```text
===== EXPENSE TRACKER =====
1. Add expense
2. Show all expenses
3. Filter by category
4. Show summary
5. Delete expense
6. Create category chart
7. Exit
===========================
Choose an option:
```

## 💵 Adding an Expense

Example:

```text
Choose an option: 1

Enter date (YYYY-MM-DD): 2026-10-01
Enter category: Food
Enter description: Lunch
Enter amount (€): 12.50

Expense added successfully with ID #1.
```

## 📊 Expense Summary

Selecting option `4` displays statistics such as:

```text
===== EXPENSE SUMMARY =====
Total expenses: €57.90
Average expense: €14.48
Largest expense: €25.00 (Dinner)

Expenses by category:
  Food: €37.50
  Transport: €10.40
  Entertainment: €10.00
============================
```

## 📈 Generating a Chart

Select:

```text
6. Create category chart
```

The application generates:

```text
reports/expenses_by_category.png
```

The chart shows the percentage of total spending for each category.

## 🧪 Running Tests

Run:

```bash
pytest
```

For detailed output:

```bash
pytest -v
```

Example:

```text
============================= test session starts =============================

tests/test_expense_tracker.py ............

============================== 12 passed =====================================
```

## 🧠 What I Learned

This project demonstrates:

* Object-Oriented Programming
* File handling
* CSV data processing
* Data validation
* Exception handling
* Type hints
* Date validation
* Data aggregation
* Data filtering
* Data visualization
* Unit testing
* Project organization

## 🔮 Future Improvements

Possible future improvements include:

* Monthly expense reports
* Budget limits
* Monthly spending comparison
* Export reports to PDF
* Interactive charts
* SQLite database support
* Web interface
* REST API
* User authentication

## 📄 License

This project is available under the MIT License.
