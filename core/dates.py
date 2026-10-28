import jdatetime


def to_jalali_str(g_date):
    """تبدیل تاریخ میلادی (datetime.date) به رشته شمسی مثل 1405-08-07"""
    j = jdatetime.date.fromgregorian(date=g_date)
    return j.strftime("%Y-%m-%d")


def get_jalali_month(date_str):
    """از رشته شمسی '1405-08-07' فقط ماه رو برمی‌گردونه: '1405-08'"""
    return date_str[:7]


def validate_jalali_date(date_str):
    """بررسی می‌کنه رشته یک تاریخ شمسی معتبر باشه. True یا False"""
    try:
        year, month, day = map(int, date_str.split("-"))
        jdatetime.date(year, month, day)
        return True
    except (ValueError, TypeError):
        return False


def today_jalali():
    """تاریخ امروز به شمسی"""
    return jdatetime.date.today().strftime("%Y-%m-%d")