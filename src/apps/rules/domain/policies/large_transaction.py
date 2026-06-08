from decimal import Decimal


def exceeds_threshold(amount: Decimal, threshold: Decimal) -> bool:
    return amount > threshold
