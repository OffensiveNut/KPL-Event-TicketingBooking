from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class TicketCategoryDTO:
    id: str
    name: str
    price: Decimal
    quota: int
    remaining_quota: int
    status: str


@dataclass
class EventSummaryDTO:
    id: str
    name: str
    start_date: date
    end_date: date
    location: str


@dataclass
class EventDetailsDTO:
    id: str
    name: str
    start_date: date
    end_date: date
    location: str
    description: str
    organizer_id: str
    ticket_categories: list[TicketCategoryDTO]
