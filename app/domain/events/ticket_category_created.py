from dataclasses import dataclass

from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.ticket_category_id import TicketCategoryId


@dataclass
class TicketCategoryCreated:
    event_id: EventId
    category_id: TicketCategoryId
    name: str
