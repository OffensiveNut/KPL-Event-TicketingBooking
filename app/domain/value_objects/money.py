from decimal import Decimal


class Money:
    def __init__(self, amount: Decimal) -> None:
        if amount < 0:
            raise ValueError("Money amount must not be negative")
        self.amount = amount
