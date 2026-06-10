from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class CreateEventSchema(BaseModel):
    event_name: str
    description: str
    start_date: date
    end_date: date
    location: str
    max_capacity: int


class CreateTicketCategorySchema(BaseModel):
    category_name: str
    price: Decimal
    quota: int
    sales_start_date: date
    sales_end_date: date


class GetAvailableEventsSchema(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    location: str | None = None
