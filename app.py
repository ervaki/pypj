import streamlit as st
import pandas as pd
import plotly.express as px

from style import inject_css
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
from core.export import to_csv_bytes, to_excel_bytes, to_pdf_bytes

st.set_page_config(page_title="داشبورد هزینه‌ها", page_icon="💰", layout="wide")
inject_css()

PALETTE = ["#4F46E5", "#7C3AED", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#EC4899"]


def style_fig(fig):
    fig.update_layout(
        font_family="Vazirmatn",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


# ---------- بنر ----------
st.markdown(
    """
    <div class="hero">
      <h1>💰 داشبورد هزینه‌ها</h1>
      <p>ثبت، تحلیل و کنترل هزینه‌های ماهانه در یک نگاه</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- سایدبار: ثبت هزینه ----------
st.sidebar.header("➕ ثبت هزینه‌ی جدید")

with st.sidebar.form("expense_form", clear_on_submit=True):
    date = st.text_input("تاریخ (شمسی)", value=today_jalali(), help="مثال: 1405-08-20")
    category = st.selectbox("دسته‌بندی", CATEGORIES)
    amount = st.number_input("مبلغ (تومان)", min_value=0, step=1000)
    description = st.text_input("توضیحات (اختیاری)")
    submitted = st.form_submit_button("ثبت هزینه", use_container_width=True)

if submitted:
    try:
        expense = create_expense(date, category, int(amount), description)
        add_expense(expense)
        st.sidebar.success("هزینه ثبت شد ✅")
    except ValueError as e:
        st.sidebar.error(str(e))

# ---------- سایدبار: بودجه ----------
st.sidebar.divider()
st.sidebar.header("🎯 تنظیم بودجه")

budgets = load_budgets()

with st.sidebar.form("budget_form"):
    b_category = st.selectbox("دسته", CATEGORIES, key="b_cat")
    b_amount = st.number_input("سقف بودجه (تومان)", min_value=0, step=100000)
    b_submitted = st.form_submit_button("ذخیره‌ی بودجه", use_container_width=True)

if b_submitted:
    budgets = set_budget(budgets, b_category, int(b_amount))
    save_budgets(budgets)
    st.sidebar.success("بودجه ذخیره شد ✅")

# ---------- داده‌ها ----------
expenses = load_expenses()

if not expenses:
    st.info("هنوز هزینه‌ای ثبت نشده. از فرم کناری اولین هزینه را ثبت کنید.")
    st.stop()

months = sorted({get_jalali_month(e["date"]) for e in expenses}, reverse=True)
selected_month = st.selectbox("📅 ماه", months)
month_expenses = filter_by_month(expenses, selected_month)

change = change_from_previous_month(expenses, selected_month)

# ---------- کارت‌های بالای صفحه ----------
k1, k2, k3, k4 = st.columns(4)
k1.metric("جمع هزینه‌های ماه", f"{total_amount(month_expenses):,}")
k2.metric("تعداد تراکنش", len(month_expenses))
k3.metric("میانگین روزانه", f"{daily_average(month_expenses):,}")
k4.metric("تغییر نسبت به ماه قبل", "—" if change is None else f"{change}%")

st.write("")

# ---------- تب‌ها ----------
tab_list, tab_analysis, tab_budget, tab_export = st.tabs(
    ["🧾 هزینه‌ها", "📈 تحلیل", "🎯 بودجه", "📤 خروجی"]
)

with tab_list:
    df = pd.DataFrame(month_expenses).rename(
        columns={
            "date": "تاریخ",
            "category": "دسته",
            "amount": "مبلغ",
            "description": "توضیحات",
        }
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab_analysis:
    top = top_category(month_expenses)
    if top:
        st.metric("پرهزینه‌ترین دسته", f"{top[0]} ({top[1]:,})")

    left, right = st.columns(2)

    by_cat = total_by_category(month_expenses)
    pie_df = pd.DataFrame({"دسته": list(by_cat.keys()), "مبلغ": list(by_cat.values())})
    pie = px.pie(
        pie_df, names="دسته", values="مبلغ", hole=0.55,
        title="سهم هر دسته", color_discrete_sequence=PALETTE,
    )
    left.plotly_chart(style_fig(pie), use_container_width=True)

    totals = monthly_totals(expenses)
    bar_df = pd.DataFrame({"ماه": list(totals.keys()), "مبلغ": list(totals.values())})
    bar = px.bar(
        bar_df, x="ماه", y="مبلغ", title="مقایسه‌ی ماه‌ها",
        color_discrete_sequence=[PALETTE[0]],
    )
    right.plotly_chart(style_fig(bar), use_container_width=True)

with tab_budget:
    if not budgets:
        st.info("هنوز بودجه‌ای تنظیم نشده. از سایدبار تنظیم کنید.")
    else:
        b1, b2 = st.columns(2)
        b1.metric("بودجه‌ی کل", f"{total_budget(budgets):,}")
        b2.metric("هزینه‌ی این ماه", f"{total_amount(month_expenses):,}")

        for cat in over_budget_categories(month_expenses, budgets):
            st.warning(f"⚠️ بودجه‌ی «{cat}» از سقف عبور کرده است!")

        status = budget_status(month_expenses, budgets)
        for cat, info in status.items():
            with st.container(border=True):
                st.write(
                    f"**{cat}**: {info['spent']:,} از {info['budget']:,} "
                    f"({info['percent']}%)"
                )
                st.progress(min(info["percent"] / 100, 1.0))

with tab_export:
    st.write("خروجی هزینه‌های ماه انتخاب‌شده:")
    e1, e2, e3 = st.columns(3)
    e1.download_button(
        "📄 دانلود CSV",
        data=to_csv_bytes(month_expenses),
        file_name=f"expenses_{selected_month}.csv",
        mime="text/csv",
        use_container_width=True,
    )
    e2.download_button(
        "📊 دانلود Excel",
        data=to_excel_bytes(month_expenses),
        file_name=f"expenses_{selected_month}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    e3.download_button(
        "📕 دانلود PDF",
        data=to_pdf_bytes(month_expenses, f"گزارش هزینه‌های {selected_month}"),
        file_name=f"expenses_{selected_month}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )