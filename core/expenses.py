from core.dates import validate_jalali_date, get_jalali_month

CATEGORIES = ["خوراک", "حمل‌ونقل", "قبوض", "تفریح", "آموزش", "سلامت", "سایر"]


def create_expense(date, category, amount, description=""):
    """یک هزینه‌ی جدید می‌سازه. اگه ورودی نامعتبر باشه ValueError می‌ده."""
    if not validate_jalali_date(date):
        raise ValueError("تاریخ نامعتبر است")
    if category not in CATEGORIES:
        raise ValueError("دسته‌بندی نامعتبر است")
    if amount <= 0:
        raise ValueError("مبلغ باید بیشتر از صفر باشد")
    return {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description,
    }


def filter_by_month(expenses, month):
    """فقط هزینه‌های یک ماه (مثلاً '1405-08') رو برمی‌گردونه."""
    return [e for e in expenses if get_jalali_month(e["date"]) == month]


def total_amount(expenses):
    """جمع کل مبلغ هزینه‌ها."""
    return sum(e["amount"] for e in expenses)


def total_by_category(expenses):
    """دیکشنری جمع هزینه به تفکیک دسته: {'خوراک': 500000, ...}"""
    result = {}
    for e in expenses:
        result[e["category"]] = result.get(e["category"], 0) + e["amount"]
    return result