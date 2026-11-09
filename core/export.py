import io

import pandas as pd
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

FONT_PATH = "fonts/Vazirmatn-Regular.ttf"

COLUMNS_FA = {
    "date": "تاریخ",
    "category": "دسته",
    "amount": "مبلغ",
    "description": "توضیحات",
}


def to_dataframe(expenses):
    """لیست هزینه‌ها را به DataFrame با ستون‌های فارسی تبدیل می‌کند."""
    df = pd.DataFrame(expenses, columns=list(COLUMNS_FA.keys()))
    return df.rename(columns=COLUMNS_FA)


def to_csv_bytes(expenses):
    """خروجی CSV (با BOM تا اکسل فارسی را درست نشان دهد)."""
    df = to_dataframe(expenses)
    return df.to_csv(index=False).encode("utf-8-sig")


def to_excel_bytes(expenses):
    """خروجی Excel (.xlsx) به‌صورت bytes."""
    df = to_dataframe(expenses)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="هزینه‌ها")
    return buffer.getvalue()


def _fa(text):
    """متن فارسی را برای نمایش درست در PDF آماده می‌کند."""
    return get_display(arabic_reshaper.reshape(str(text)))


def to_pdf_bytes(expenses, title="گزارش هزینه‌ها"):
    """خروجی PDF جدول هزینه‌ها به‌صورت bytes."""
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Vazir", "", FONT_PATH)
    pdf.set_font("Vazir", size=16)
    pdf.cell(0, 12, _fa(title), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Vazir", size=11)
    widths = [35, 40, 40, 75]
    headers = ["توضیحات", "مبلغ", "دسته", "تاریخ"]

    for w, h in zip(widths[::-1], headers):
        pdf.cell(w, 10, _fa(h), border=1, align="C")
    pdf.ln()

    for e in expenses:
        row = [e["description"], f"{e['amount']:,}", e["category"], e["date"]]
        for w, value in zip(widths[::-1], row):
            pdf.cell(w, 9, _fa(value), border=1, align="C")
        pdf.ln()

    pdf.ln(4)
    total = sum(e["amount"] for e in expenses)
    pdf.cell(0, 10, _fa(f"جمع کل: {total:,} تومان"), align="R")

    return bytes(pdf.output())