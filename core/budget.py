from core.expenses import CATEGORIES, total_by_category


def set_budget(budgets, category, amount):
    """بودجه‌ی یک دسته رو تنظیم می‌کنه (دیکشنری جدید برمی‌گردونه)."""
    if category not in CATEGORIES:
        raise ValueError("دسته‌بندی نامعتبر است")
    if amount < 0:
        raise ValueError("بودجه نمی‌تواند منفی باشد")
    new_budgets = dict(budgets)
    new_budgets[category] = amount
    return new_budgets


def total_budget(budgets):
    """جمع بودجه‌ی همه‌ی دسته‌ها (بودجه‌ی کلی)."""
    return sum(budgets.values())


def budget_status(expenses, budgets):
    """
    برای هر دسته‌ای که بودجه داره وضعیت رو برمی‌گردونه:
    {'خوراک': {'budget': 3000000, 'spent': 500000,
               'remaining': 2500000, 'percent': 16.7, 'over': False}}
    """
    spent = total_by_category(expenses)
    result = {}
    for category, budget in budgets.items():
        s = spent.get(category, 0)
        percent = round(s / budget * 100, 1) if budget > 0 else 0.0
        result[category] = {
            "budget": budget,
            "spent": s,
            "remaining": budget - s,
            "percent": percent,
            "over": s > budget,
        }
    return result


def over_budget_categories(expenses, budgets):
    """لیست دسته‌هایی که از بودجه عبور کرده‌اند."""
    status = budget_status(expenses, budgets)
    return [c for c, info in status.items() if info["over"]]