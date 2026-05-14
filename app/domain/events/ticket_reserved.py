from dataclasses import dataclass

from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.ticket_category_id import TicketCategoryId


@dataclass
class TicketReserved:
    booking_id: BookingId
    event_id: EventId
    ticket_category_id: TicketCategoryId
