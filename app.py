import streamlit as st
import pandas as pd
import plotly.express as px

from core.export import to_csv_bytes, to_excel_bytes, to_pdf_bytes
from core.dates import today_jalali, get_jalali_month
from core.expenses import (
    CATEGORIES,
    create_expense,
    filter_by_month,
    total_amount,
    total_by_category,
)
from core.analysis import (
    monthly_totals,
    top_category,
    change_from_previous_month,
    daily_average,
)
from core.budget import (
    set_budget,
    total_budget,
    budget_status,
    over_budget_categories,
)
from core.storage import load_expenses, add_expense, load_budgets, save_budgets

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

# ---------- فرم بودجه (سایدبار) ----------
st.sidebar.divider()
st.sidebar.header("تنظیم بودجه‌ی ماهانه")

budgets = load_budgets()

with st.sidebar.form("budget_form"):
    b_category = st.selectbox("دسته", CATEGORIES, key="b_cat")
    b_amount = st.number_input("سقف بودجه (تومان)", min_value=0, step=100000)
    b_submitted = st.form_submit_button("ذخیره‌ی بودجه")

if b_submitted:
    budgets = set_budget(budgets, b_category, int(b_amount))
    save_budgets(budgets)
    st.sidebar.success("بودجه ذخیره شد ✅")

# ---------- نمایش داده‌ها ----------
expenses = load_expenses()

if not expenses:
    st.info("هنوز هزینه‌ای ثبت نشده. از فرم کناری اولین هزینه را ثبت کنید.")
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

# ---------- وضعیت بودجه ----------
st.divider()
st.subheader("وضعیت بودجه")

if not budgets:
    st.info("هنوز بودجه‌ای تنظیم نشده. از سایدبار تنظیم کنید.")
else:
    st.metric("بودجه‌ی کل ماه", f"{total_budget(budgets):,} تومان")

    for cat in over_budget_categories(month_expenses, budgets):
        st.warning(f"⚠️ بودجه‌ی «{cat}» از سقف عبور کرده است!")

    status = budget_status(month_expenses, budgets)
    for cat, info in status.items():
        st.write(f"**{cat}**: {info['spent']:,} از {info['budget']:,} ({info['percent']}%)")
        st.progress(min(info["percent"] / 100, 1.0))

        # ---------- خروجی داده ----------
        st.divider()
        st.subheader("خروجی داده")

        e1, e2, e3 = st.columns(3)
        e1.download_button(
            "📄 دانلود CSV",
            data=to_csv_bytes(month_expenses),
            file_name=f"expenses_{selected_month}.csv",
            mime="text/csv",
        )
        e2.download_button(
            "📊 دانلود Excel",
            data=to_excel_bytes(month_expenses),
            file_name=f"expenses_{selected_month}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        e3.download_button(
            "📕 دانلود PDF",
            data=to_pdf_bytes(month_expenses, f"گزارش هزینه‌های {selected_month}"),
            file_name=f"expenses_{selected_month}.pdf",
            mime="application/pdf",
        )