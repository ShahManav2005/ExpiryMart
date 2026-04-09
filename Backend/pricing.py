# pricing.py  ← new file, put in your backend folder

def calculate_buying_price(mrp, months_left):
    """
    Rule: What company pays to seller
    1 month  → 40% of MRP
    2 months → 45% of MRP
    3 months → 50% of MRP  (max cap)
    """
    if months_left <= 1:
        percent = 0.40
    elif months_left == 2:
        percent = 0.45
    else:
        percent = 0.50   # max cap at 3+ months = 50%

    return round(mrp * percent, 2)


def calculate_selling_price(buying_price, months_left):
    """
    Rule: What buyer pays to company
    1-2 months → buying_price × 1.80  (+80%)
    2-3 months → buying_price × 1.85  (+85%)
    3+ months  → buying_price × 1.90  (+90%)
    """
    if months_left <= 2:
        markup = 1.80
    elif months_left <= 3:
        markup = 1.85
    else:
        markup = 1.90

    return round(buying_price * markup, 2)