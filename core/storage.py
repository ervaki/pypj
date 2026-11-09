import csv
import json
import os

FIELDS = ["date", "category", "amount", "description"]
DEFAULT_PATH = os.path.join("data", "expenses.csv")
BUDGET_PATH = os.path.join("data", "budgets.json")


def save_expenses(expenses, path=DEFAULT_PATH):
    """کل لیست هزینه‌ها رو توی فایل CSV می‌نویسه."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def load_expenses(path=DEFAULT_PATH):
    """هزینه‌ها رو از CSV می‌خونه. اگه فایل نبود، لیست خالی برمی‌گردونه."""
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        expenses = []
        for row in reader:
            row["amount"] = int(row["amount"])
            expenses.append(row)
        return expenses


def add_expense(expense, path=DEFAULT_PATH):
    """یک هزینه رو به فایل اضافه می‌کنه."""
    expenses = load_expenses(path)
    expenses.append(expense)
    save_expenses(expenses, path)


def save_budgets(budgets, path=BUDGET_PATH):
    """بودجه‌ها رو توی فایل JSON ذخیره می‌کنه."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(budgets, f, ensure_ascii=False, indent=2)


def load_budgets(path=BUDGET_PATH):
    """بودجه‌ها رو می‌خونه. اگه فایل نبود، دیکشنری خالی."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)