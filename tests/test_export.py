import os
import pytest

from core.export import (
    to_dataframe,
    to_csv_bytes,
    to_excel_bytes,
    to_pdf_bytes,
    FONT_PATH,
)
from core.expenses import create_expense


def sample():
    return [
        create_expense("1405-08-01", "خوراک", 100000, "ناهار"),
        create_expense("1405-08-02", "قبوض", 250000),
    ]


def test_to_dataframe_columns():
    df = to_dataframe(sample())
    assert list(df.columns) == ["تاریخ", "دسته", "مبلغ", "توضیحات"]
    assert len(df) == 2


def test_to_csv_bytes_contains_data():
    data = to_csv_bytes(sample()).decode("utf-8-sig")
    assert "خوراک" in data
    assert "100000" in data


def test_to_excel_bytes_is_xlsx():
    data = to_excel_bytes(sample())
    assert data[:2] == b"PK"  # فایل xlsx یک zip است


@pytest.mark.skipif(not os.path.exists(FONT_PATH), reason="فونت فارسی موجود نیست")
def test_to_pdf_bytes_is_pdf():
    data = to_pdf_bytes(sample())
    assert data[:4] == b"%PDF"