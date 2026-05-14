from dataclasses import dataclass

from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.ticket_category_id import TicketCategoryId


@dataclass
class TicketCategoryDisabled:
    category_id: TicketCategoryId
    event_id: EventId
