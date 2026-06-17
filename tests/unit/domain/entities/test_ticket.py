"""US 13: Ticket check-in rules."""
import pytest

from app.domain.entities.ticket import Ticket
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.event_id import EventId


class TestTicketDoubleCheckin:
    def test_checked_in_ticket_cannot_check_in_again(self):
        ticket = Ticket(
            booking_id=BookingId("book-1"),
            event_id=EventId("event-1"),
        )
        ticket.check_in()
        with pytest.raises(ValueError, match="not active"):
            ticket.check_in()
