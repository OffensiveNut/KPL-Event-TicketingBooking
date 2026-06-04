from dataclasses import dataclass
from decimal import Decimal


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


@dataclass
class ParticipantTicketDetailsDTO:
    ticket_code: str
    is_check_in: bool


@dataclass
class ParticipantDTO:
    customer_name: str
    ticket_category_name: str
    ticket_details: list[ParticipantTicketDetailsDTO]
