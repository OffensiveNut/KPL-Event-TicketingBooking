from datetime import date

import pytest

from app.domain.entities.ticket_category import TicketCategory
from app.domain.events.ticket_category_created import TicketCategoryCreated
from app.domain.events.ticket_category_disabled import TicketCategoryDisabled
from app.domain.value_objects.event_status import EventStatus


def test_create_ticket_category_success(valid_ticket_category):
    """
    US 4 Acceptance Criteria 1 & 2:
    - The Event Organizer can create ticket categories such as Regular, VIP, or Early Bird.
    - Each ticket category must have a name, price, quota, sales start date, and sales end date.
    """
    assert valid_ticket_category.name == "Regular Ticket"
    assert valid_ticket_category.price == 150.0
    assert valid_ticket_category.quota == 50
    assert valid_ticket_category.sales_period.start_date == date(2077, 1, 1)
    assert valid_ticket_category.sales_period.end_date == date(2077, 9, 30)
    assert valid_ticket_category.is_active is True


def test_create_ticket_category_invalid_price():
    """US 4 Acceptance Criteria 3: The ticket price cannot be less than zero."""
    with pytest.raises(ValueError, match="Price must be non-negative"):
        TicketCategory(
            name="Freebie",
            price=-10.0,
            quota=10,
            sales_start_date=date(2077, 1, 1),
            sales_end_date=date(2077, 1, 15),
        )


def test_create_ticket_category_invalid_quota():
    """US 4 Acceptance Criteria 4: The ticket quota must be greater than zero."""
    with pytest.raises(ValueError, match="Quota must be greater than 0"):
        TicketCategory(
            name="Empty",
            price=10.0,
            quota=0,
            sales_start_date=date(2077, 1, 1),
            sales_end_date=date(2077, 1, 15),
        )


def test_add_ticket_category_invalid_sales_period(valid_event):
    """US 4 Acceptance Criteria 5: The ticket sales period must end before or at the event start date."""
    late_category = TicketCategory(
        "Late",
        100.0,
        50,
        date(2077, 1, 1),
        date(2077, 10, 10),  # 10-10 > 10-01 (event start)
    )
    with pytest.raises(
        ValueError, match="Sales period must end before or at the event start date"
    ):
        valid_event.add_ticket_category(late_category)


def test_add_ticket_category_exceeds_capacity(valid_event):
    """US 4 Acceptance Criteria 6: The total quota of all ticket categories must not exceed the maximum event capacity."""
    large_category = TicketCategory(
        "VIP", 200.0, 150, date(2077, 1, 1), date(2077, 9, 30)
    )  # quota 150 > max_capacity 100

    with pytest.raises(ValueError, match="Total quota exceeds max capacity"):
        valid_event.add_ticket_category(large_category)


def test_add_ticket_category_raises_event(valid_event, valid_ticket_category):
    """US 4 Acceptance Criteria 7: After a ticket category is created, the system raises the domain event TicketCategoryCreated."""
    valid_event.add_ticket_category(valid_ticket_category)

    assert valid_ticket_category in valid_event._ticket_categories

    # Check that TicketCategoryCreated was raised
    category_created_events = [
        e for e in valid_event._domain_events if isinstance(e, TicketCategoryCreated)
    ]
    assert len(category_created_events) == 1
    assert category_created_events[0].name == "Regular Ticket"


def test_event_disable_ticket_category_fails_if_completed(
    valid_event, valid_ticket_category
):
    """US 5 Acceptance Criteria 1: A ticket category can be disabled if the event has not been completed."""
    valid_event.add_ticket_category(valid_ticket_category)

    # Force event to be COMPLETED
    valid_event.status = EventStatus.COMPLETED

    with pytest.raises(
        ValueError, match="Cannot disable ticket category for a completed event"
    ):
        valid_event.disable_ticket_category(valid_ticket_category.id)


def test_ticket_category_retained_for_historical_purposes(
    valid_event, valid_ticket_category
):
    """
    US 5 Acceptance Criteria 2: A ticket category that already has bookings must still be stored for historical purposes.
    (At the domain layer, disabling a category just marks it inactive but keeps it in the collection).
    """
    valid_event.add_ticket_category(valid_ticket_category)
    valid_event.disable_ticket_category(valid_ticket_category.id)

    # It must remain in the event's collection
    assert valid_ticket_category in valid_event._ticket_categories
    assert valid_ticket_category.is_active is False


def test_cannot_purchase_inactive_ticket_category():
    """
    US 5 Acceptance Criteria 3: Customers cannot purchase tickets from an inactive ticket category.
    (This is typically handled by the Booking use case, but we document it here for completeness).
    """
    pytest.skip("To be implemented in the Booking usecase test")


def test_event_disable_ticket_category_raises_event(valid_event, valid_ticket_category):
    """US 5 Acceptance Criteria 4: After a ticket category is disabled, the system raises the domain event TicketCategoryDisabled."""
    valid_event.add_ticket_category(valid_ticket_category)
    valid_event.disable_ticket_category(valid_ticket_category.id)

    category_disabled_events = [
        e for e in valid_event._domain_events if isinstance(e, TicketCategoryDisabled)
    ]
    assert len(category_disabled_events) == 1
    assert category_disabled_events[0].category_id == valid_ticket_category.id
