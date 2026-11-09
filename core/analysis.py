from core.expenses import filter_by_month, total_amount, total_by_category


def monthly_totals(expenses):
    """جمع هزینه‌ی هر ماه به‌ترتیب زمانی: {'1405-07': 500000, '1405-08': 800000}"""
    months = sorted({e["date"][:7] for e in expenses})
    return {m: total_amount(filter_by_month(expenses, m)) for m in months}


def top_category(expenses):
    """پرهزینه‌ترین دسته: (نام، مبلغ). اگه هزینه‌ای نباشه None."""
    totals = total_by_category(expenses)
    if not totals:
        return None
    name = max(totals, key=totals.get)
    return name, totals[name]


def change_from_previous_month(expenses, month):
    """درصد تغییر نسبت به ماه قبل. اگه ماه قبل داده نداشت None."""
    totals = monthly_totals(expenses)
    months = list(totals)
    if month not in months:
        return None
    index = months.index(month)
    if index == 0:
        return None
    previous = totals[months[index - 1]]
    if previous == 0:
        return None
    return round((totals[month] - previous) / previous * 100, 1)


def daily_average(expenses, days_in_month=30):
    """میانگین هزینه‌ی روزانه."""
    if days_in_month <= 0:
        raise ValueError("تعداد روز باید مثبت باشد")
    return round(total_amount(expenses) / days_in_month)