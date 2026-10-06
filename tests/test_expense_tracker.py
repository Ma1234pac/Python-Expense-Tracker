import pytest

from src.expense_tracker import ExpenseTracker


def test_add_expense(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    expense = manager.add_expense(
        "2026-10-01",
        "Food",
        "Lunch",
        12.50
    )

    assert expense["id"] == 1
    assert expense["category"] == "Food"
    assert expense["amount"] == 12.50


def test_add_multiple_expenses(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    manager.add_expense(
        "2026-10-01",
        "Food",
        "Lunch",
        10.00
    )

    manager.add_expense(
        "2026-10-02",
        "Transport",
        "Bus",
        2.50
    )

    expenses = manager.get_expenses()

    assert len(expenses) == 2


def test_total_expenses(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    manager.add_expense(
        "2026-10-01",
        "Food",
        "Lunch",
        10.00
    )

    manager.add_expense(
        "2026-10-02",
        "Food",
        "Dinner",
        20.00
    )

    assert manager.get_total() == 30.00


def test_average_expense(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    manager.add_expense(
        "2026-10-01",
        "Food",
        "Lunch",
        10.00
    )

    manager.add_expense(
        "2026-10-02",
        "Transport",
        "Bus",
        20.00
    )

    assert manager.get_average() == 15.00


def test_filter_by_category(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    manager.add_expense(
        "2026-10-01",
        "Food",
        "Lunch",
        10.00
    )

    manager.add_expense(
        "2026-10-02",
        "Transport",
        "Bus",
        2.50
    )

    food_expenses = manager.get_expenses("Food")

    assert len(food_expenses) == 1
    assert food_expenses[0]["category"] == "Food"


def test_total_by_category(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    manager.add_expense(
        "2026-10-01",
        "Food",
        "Lunch",
        10.00
    )

    manager.add_expense(
        "2026-10-02",
        "Food",
        "Dinner",
        20.00
    )

    manager.add_expense(
        "2026-10-03",
        "Transport",
        "Bus",
        5.00
    )

    totals = manager.get_total_by_category()

    assert totals["Food"] == 30.00
    assert totals["Transport"] == 5.00


def test_largest_expense(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    manager.add_expense(
        "2026-10-01",
        "Food",
        "Lunch",
        10.00
    )

    manager.add_expense(
        "2026-10-02",
        "Shopping",
        "Shoes",
        80.00
    )

    largest = manager.get_largest_expense()

    assert largest["description"] == "Shoes"
    assert largest["amount"] == 80.00


def test_delete_expense(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    expense = manager.add_expense(
        "2026-10-01",
        "Food",
        "Lunch",
        10.00
    )

    result = manager.delete_expense(
        expense["id"]
    )

    assert result is True
    assert len(manager.get_expenses()) == 0


def test_invalid_date(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    with pytest.raises(ValueError):
        manager.add_expense(
            "01-10-2026",
            "Food",
            "Lunch",
            10.00
        )


def test_invalid_amount(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    with pytest.raises(ValueError):
        manager.add_expense(
            "2026-10-01",
            "Food",
            "Lunch",
            -10.00
        )


def test_persistence(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager1 = ExpenseTracker(str(file_path))

    manager1.add_expense(
        "2026-10-01",
        "Food",
        "Lunch",
        12.50
    )

    manager2 = ExpenseTracker(str(file_path))

    expenses = manager2.get_expenses()

    assert len(expenses) == 1
    assert expenses[0]["description"] == "Lunch"
    assert expenses[0]["amount"] == 12.50


def test_empty_tracker(tmp_path):
    file_path = tmp_path / "expenses.csv"

    manager = ExpenseTracker(str(file_path))

    assert manager.get_total() == 0.00
    assert manager.get_average() == 0.00
    assert manager.get_largest_expense() is None
