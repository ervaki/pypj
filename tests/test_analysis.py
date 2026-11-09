from core.analysis import (
    monthly_totals,
    top_category,
    change_from_previous_month,
    daily_average,
)
from core.expenses import create_expense


def sample():
    return [
        create_expense("1405-07-05", "خوراک", 100000),
        create_expense("1405-08-01", "خوراک", 150000),
        create_expense("1405-08-10", "قبوض", 50000),
    ]


def test_monthly_totals():
    assert monthly_totals(sample()) == {"1405-07": 100000, "1405-08": 200000}


def test_top_category():
    assert top_category(sample()) == ("خوراک", 250000)


def test_top_category_empty():
    assert top_category([]) is None


def test_change_from_previous_month():
    assert change_from_previous_month(sample(), "1405-08") == 100.0


def test_change_first_month_is_none():
    assert change_from_previous_month(sample(), "1405-07") is None


def test_daily_average():
    assert daily_average(sample()[1:], 10) == 20000