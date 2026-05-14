import uuid

from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.ticket_id import TicketId
from app.domain.value_objects.ticket_status import TicketStatus


class Ticket:
    def __init__(
        self,
        booking_id: BookingId,
        event_id: EventId,
    ):
        self.id = TicketId(str(uuid.uuid4()))
        self.ticket_code = TicketCode(str(uuid.uuid4()))
        self.booking_id = booking_id
        self.event_id = event_id
        self.status = TicketStatus.ACTIVE

    def check_in(self) -> None:
        if self.status != TicketStatus.ACTIVE:
            raise ValueError("Cannot check in a ticket that is not active")
        self.status = TicketStatus.CHECKED_IN
