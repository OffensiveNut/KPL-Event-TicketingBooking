from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BookingTotalPrice:
    total_price: Decimal


@dataclass
class TicketSummary:
    ticket_id: str
    ticket_code: str
    event_id: str
    status: str
