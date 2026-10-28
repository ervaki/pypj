import pytest
from core.expenses import (
    create_expense,
    filter_by_month,
    total_amount,
    total_by_category,
)


def sample_data():
    return [
        create_expense("1405-08-01", "خوراک", 100000),
        create_expense("1405-08-05", "خوراک", 200000),
        create_expense("1405-08-10", "حمل‌ونقل", 50000),
        create_expense("1405-09-02", "قبوض", 300000),
    ]


def test_create_expense_valid():
    e = create_expense("1405-08-01", "خوراک", 100000, "ناهار")
    assert e["amount"] == 100000
    assert e["description"] == "ناهار"


def test_create_expense_invalid_amount():
    with pytest.raises(ValueError):
        create_expense("1405-08-01", "خوراک", 0)


def test_create_expense_invalid_date():
    with pytest.raises(ValueError):
        create_expense("1405-13-01", "خوراک", 1000)


def test_create_expense_invalid_category():
    with pytest.raises(ValueError):
        create_expense("1405-08-01", "نامعتبر", 1000)


def test_filter_by_month():
    result = filter_by_month(sample_data(), "1405-08")
    assert len(result) == 3


def test_total_amount():
    assert total_amount(sample_data()) == 650000


def test_total_by_category():
    result = total_by_category(sample_data())
    assert result["خوراک"] == 300000
    assert result["حمل‌ونقل"] == 50000