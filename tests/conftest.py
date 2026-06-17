from datetime import date, datetime, timedelta
from decimal import Decimal

import pytest

from app.domain.aggregates.booking import Booking
from app.domain.aggregates.event import Event
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.money import Money
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.user_id import UserId


@pytest.fixture
def valid_event():
    return Event(
        event_name="Test Event",
        description="Test Description",
        start_date=date(2026, 7, 1),
        end_date=date(2026, 7, 2),
        location="Test Location",
        max_capacity=100,
        event_organizer=UserId("org-1"),
    )


@pytest.fixture
def valid_booking():
    return Booking(
        ticket_category_id=TicketCategoryId("cat-1"),
        ticket_category_name="Regular",
        event_id=EventId("event-1"),
        ticket_quantity=2,
        ticket_price=Money(Decimal("100")),
        service_fee=Money(Decimal("0")),
        customer_id=UserId("cust-1"),
        customer_name="Customer",
    )
