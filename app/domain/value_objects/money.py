from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount must not be negative")

    def multiply(self, factor: Decimal | int) -> "Money":
        return Money(self.amount * factor)

    def add(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)
