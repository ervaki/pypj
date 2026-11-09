import pytest
from core.budget import (
    set_budget,
    total_budget,
    budget_status,
    over_budget_categories,
)
from core.expenses import create_expense


def sample_expenses():
    return [
        create_expense("1405-08-01", "خوراک", 400000),
        create_expense("1405-08-02", "خوراک", 700000),
        create_expense("1405-08-03", "حمل‌ونقل", 50000),
    ]


def test_set_budget():
    b = set_budget({}, "خوراک", 1000000)
    assert b == {"خوراک": 1000000}


def test_set_budget_does_not_modify_original():
    original = {"خوراک": 1}
    set_budget(original, "قبوض", 5)
    assert original == {"خوراک": 1}


def test_set_budget_invalid_category():
    with pytest.raises(ValueError):
        set_budget({}, "نامعتبر", 100)


def test_set_budget_negative():
    with pytest.raises(ValueError):
        set_budget({}, "خوراک", -5)


def test_total_budget():
    assert total_budget({"خوراک": 100, "قبوض": 50}) == 150


def test_budget_status_values():
    budgets = {"خوراک": 1000000, "حمل‌ونقل": 100000}
    status = budget_status(sample_expenses(), budgets)
    assert status["خوراک"]["spent"] == 1100000
    assert status["خوراک"]["over"] is True
    assert status["حمل‌ونقل"]["remaining"] == 50000
    assert status["حمل‌ونقل"]["percent"] == 50.0


def test_over_budget_categories():
    budgets = {"خوراک": 1000000, "حمل‌ونقل": 100000}
    assert over_budget_categories(sample_expenses(), budgets) == ["خوراک"]