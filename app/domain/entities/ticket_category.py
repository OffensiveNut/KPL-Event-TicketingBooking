import uuid
from datetime import date

from app.domain.events.ticket_category_created import TicketCategoryCreated
from app.domain.value_objects.sales_period import SalesPeriod


class TicketCategory:
    def __init__(
        self,
        name: str,
        price: float,
        quota: int,
        sales_start_date: date,
        sales_end_date: date,
    ):
        if price < 0:
            raise ValueError("Price must be non-negative")
        if quota <= 0:
            raise ValueError("Quota must be greater than 0")

        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.quota = quota
        self.sales_period = SalesPeriod(sales_start_date, sales_end_date)
        self.is_active = True

        self._domain_events: list = []
        self._domain_events.append(TicketCategoryCreated(id=self.id, name=self.name))
