"""US 15: Refund request rules — application layer handler tests."""
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.application.usecases.refund.command_handlers import (
    RequestRefundCommandHandler,
)
from app.application.usecases.refund.commands import RequestRefundCommand
from app.domain.aggregates.booking import Booking
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.event_status import EventStatus
from app.domain.value_objects.money import Money
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.user_id import UserId


class TestRefundRequestWithCheckedInTicket:
    def test_refund_request_fails_when_ticket_checked_in(self):
        booking = Booking(
            ticket_category_id=TicketCategoryId("cat-1"),
            ticket_category_name="Regular",
            event_id=EventId("event-1"),
            ticket_quantity=1,
            ticket_price=Money(Decimal("100")),
            service_fee=Money(Decimal("0")),
            customer_id=UserId("cust-1"),
            customer_name="Customer",
        )
        booking.payment_deadline = datetime.now() + timedelta(hours=1)
        booking.pay(Money(Decimal("100")))
        booking.tickets[0].check_in()

        booking_repo = MagicMock()
        booking_repo.get_by_id.return_value = booking

        event = MagicMock()
        event.status = EventStatus.CANCELLED
        event_repo = MagicMock()
        event_repo.get_by_id.return_value = event

        refund_repo = MagicMock()

        handler = RequestRefundCommandHandler(booking_repo, event_repo, refund_repo)
        command = RequestRefundCommand(booking_id=booking.id, event_id=event.id)

        with pytest.raises(ValueError, match="checked-in"):
            handler.handle(command)
