import datetime
from core.dates import to_jalali_str, get_jalali_month, validate_jalali_date


def test_to_jalali_str():
    assert to_jalali_str(datetime.date(2026, 3, 21)) == "1405-01-01"


def test_get_jalali_month():
    assert get_jalali_month("1405-08-07") == "1405-08"


def test_validate_valid_date():
    assert validate_jalali_date("1405-08-07") is True


def test_validate_invalid_month():
    assert validate_jalali_date("1405-13-01") is False


def test_validate_invalid_format():
    assert validate_jalali_date("abc") is False 