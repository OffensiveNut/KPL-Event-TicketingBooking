import uuid
from datetime import date
from decimal import Decimal

import pytest

from app.domain.aggregates.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.domain.value_objects.user_id import UserId


@pytest.fixture
def valid_event():
    """Returns a valid Draft Event with max capacity 100."""
    return Event(
        event_name="Schematics REEVA 2077",
        description="An event by informatics ITS.",
        start_date=date(2077, 10, 1),
        end_date=date(2077, 12, 2),
        location="ITS Surabaya",
        max_capacity=100,
        event_organizer=UserId(str(uuid.uuid4())),
    )


@pytest.fixture
def valid_ticket_category():
    """Returns a valid TicketCategory with quota 50."""
    return TicketCategory(
        name="Regular Ticket",
        price=Decimal(150.0),
        quota=50,
        sales_start_date=date(2077, 1, 1),
        sales_end_date=date(2077, 9, 30),
    )
