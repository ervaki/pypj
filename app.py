import plotly.express as px

from core.analysis import (
    monthly_totals,
    top_category,
    change_from_previous_month,
    daily_average,
)
from core.expenses import total_by_category

import streamlit as st
import pandas as pd

from core.dates import today_jalali, get_jalali_month
from core.expenses import (
    CATEGORIES,
    create_expense,
    filter_by_month,
    total_amount,
)
from core.storage import load_expenses, add_expense

st.set_page_config(page_title="داشبورد هزینه‌ها", page_icon="💰", layout="wide")
st.title("💰 داشبورد ثبت و تحلیل هزینه‌ها")

# ---------- فرم ثبت هزینه (سایدبار) ----------
st.sidebar.header("ثبت هزینه‌ی جدید")

with st.sidebar.form("expense_form", clear_on_submit=True):
    date = st.text_input("تاریخ (شمسی)", value=today_jalali(), help="مثال: 1405-08-20")
    category = st.selectbox("دسته‌بندی", CATEGORIES)
    amount = st.number_input("مبلغ (تومان)", min_value=0, step=1000)
    description = st.text_input("توضیحات (اختیاری)")
    submitted = st.form_submit_button("ثبت")

if submitted:
    try:
        expense = create_expense(date, category, int(amount), description)
        add_expense(expense)
        st.sidebar.success("هزینه ثبت شد ✅")
    except ValueError as e:
        st.sidebar.error(str(e))

# ---------- نمایش داده‌ها ----------
expenses = load_expenses()

if not expenses:
    st.info("هنوز هزینه‌ای ثبت نشده. از فرم سمت راست/چپ اولین هزینه را ثبت کنید.")
    st.stop()

months = sorted({get_jalali_month(e["date"]) for e in expenses}, reverse=True)
selected_month = st.selectbox("ماه", months)

month_expenses = filter_by_month(expenses, selected_month)

col1, col2 = st.columns(2)
col1.metric("جمع هزینه‌های ماه", f"{total_amount(month_expenses):,} تومان")
col2.metric("تعداد تراکنش", len(month_expenses))

st.subheader("لیست هزینه‌ها")
df = pd.DataFrame(month_expenses)
df = df.rename(
    columns={
        "date": "تاریخ",
        "category": "دسته",
        "amount": "مبلغ",
        "description": "توضیحات",
    }
)
st.dataframe(df, use_container_width=True, hide_index=True)

# ---------- تحلیل ماهانه ----------
st.divider()
st.subheader("تحلیل ماهانه")

change = change_from_previous_month(expenses, selected_month)
top = top_category(month_expenses)

c1, c2, c3 = st.columns(3)
c1.metric(
    "تغییر نسبت به ماه قبل",
    "—" if change is None else f"{change}%",
)
c2.metric(
    "پرهزینه‌ترین دسته",
    "—" if top is None else f"{top[0]} ({top[1]:,})",
)
c3.metric("میانگین روزانه", f"{daily_average(month_expenses):,} تومان")

# ---------- نمودارها ----------
st.subheader("نمودارها")
left, right = st.columns(2)

by_cat = total_by_category(month_expenses)
pie_df = pd.DataFrame({"دسته": list(by_cat.keys()), "مبلغ": list(by_cat.values())})
left.plotly_chart(
    px.pie(pie_df, names="دسته", values="مبلغ", title="سهم هر دسته"),
    use_container_width=True,
)

totals = monthly_totals(expenses)
bar_df = pd.DataFrame({"ماه": list(totals.keys()), "مبلغ": list(totals.values())})
right.plotly_chart(
    px.bar(bar_df, x="ماه", y="مبلغ", title="مقایسه‌ی ماه‌ها"),
    use_container_width=True,
)