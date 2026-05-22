from dataclasses import dataclass
from decimal import Decimal

from app.domain.value_objects.event_id import EventId


@dataclass
class TicketCategorySalesDTO:
    name: str
    price: Decimal
    quota_sold: int


@dataclass
class BookingReportDTO:
    status: str
    total_bookings: int
    total_revenue: Decimal


@dataclass
class EventSalesReportDTO:
    name: str
    ticket_categories: list[TicketCategorySalesDTO]
    bookings: list[BookingReportDTO]
