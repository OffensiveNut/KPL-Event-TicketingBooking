from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.user_id import UserId


@dataclass
class CreateEventCommand:
    event_organizer: UserId
    event_name: str
    description: str
    start_date: date
    end_date: date
    location: str
    max_capacity: int


@dataclass
class PublishEventCommand:
    event_id: EventId


@dataclass
class CancelEventCommand:
    event_id: EventId


@dataclass
class CreateTicketCategoryCommand:
    event_id: EventId
    category_name: str
    price: Decimal
    quota: int
    sales_start_date: date
    sales_end_date: date


@dataclass
class DisableTicketCategoryCommand:
    event_id: EventId
    category_id: TicketCategoryId
