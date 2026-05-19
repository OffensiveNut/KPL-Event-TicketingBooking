import uuid
from datetime import date
from decimal import Decimal

from app.domain.value_objects.money import Money
from app.domain.value_objects.sales_period import SalesPeriod
from app.domain.value_objects.ticket_category_id import TicketCategoryId


class TicketCategory:
    def __init__(
        self,
        name: str,
        price: Decimal,
        quota: int,
        sales_start_date: date,
        sales_end_date: date,
    ):
        if quota <= 0:
            raise ValueError("Quota must be greater than 0")

        self.id = TicketCategoryId(str(uuid.uuid4()))
        self.name = name
        self.price = Money(price)
        self.quota = quota
        self.remaining_quota = quota
        self.sales_period = SalesPeriod(sales_start_date, sales_end_date)
        self.is_active = True

    def disable(self):
        self.is_active = False

    def reserve(self, quantity: int):
        if quantity > self.quota:
            raise ValueError("Quantity exceeds quota")
        self.quota -= quantity

    def release(self, quantity: int):
        self.quota += quantity
