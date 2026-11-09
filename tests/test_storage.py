from core.storage import (
    save_expenses,
    load_expenses,
    add_expense,
    save_budgets,
    load_budgets,
)
from core.expenses import create_expense


def test_load_missing_file_returns_empty(tmp_path):
    path = tmp_path / "none.csv"
    assert load_expenses(str(path)) == []


def test_save_and_load_roundtrip(tmp_path):
    path = str(tmp_path / "e.csv")
    data = [
        create_expense("1405-08-01", "خوراک", 100000, "ناهار"),
        create_expense("1405-08-02", "قبوض", 250000),
    ]
    save_expenses(data, path)
    loaded = load_expenses(path)
    assert loaded == data


def test_add_expense_appends(tmp_path):
    path = str(tmp_path / "e.csv")
    add_expense(create_expense("1405-08-01", "خوراک", 1000), path)
    add_expense(create_expense("1405-08-02", "تفریح", 2000), path)
    assert len(load_expenses(path)) == 2


def test_budgets_missing_file(tmp_path):
    assert load_budgets(str(tmp_path / "b.json")) == {}


def test_budgets_roundtrip(tmp_path):
    path = str(tmp_path / "b.json")
    save_budgets({"خوراک": 3000000, "قبوض": 500000}, path)
    assert load_budgets(path) == {"خوراک": 3000000, "قبوض": 500000}