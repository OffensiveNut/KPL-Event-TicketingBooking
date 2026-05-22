from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BookingTotalPriceDTO:
    total_price: Decimal


@dataclass
class TicketSummaryDTO:
    ticket_id: str
    ticket_code: str
    event_id: str
    status: str
