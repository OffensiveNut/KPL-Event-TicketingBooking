from datetime import date

import pytest

from app.domain.aggregates.event import Event
from app.domain.events.event_cancelled import EventCancelled
from app.domain.events.event_created import EventCreated
from app.domain.events.event_published import EventPublished
from app.domain.value_objects.event_status import EventStatus


def test_create_event_success(valid_event):
    """
    US 1 Acceptance Criteria:
    - Given I am authenticated as an Event Organizer, when I enter the event name...
    - A newly created event must have the status Draft.
    - After the event is created, the system raises the domain event EventCreated.
    """
    assert valid_event.status == EventStatus.DRAFT

    event_created_events = [
        e for e in valid_event._domain_events if isinstance(e, EventCreated)
    ]
    assert len(event_created_events) == 1
    assert event_created_events[0].event_name == "Schematics REEVA 2077"


def test_create_event_invalid_date():
    """US 1 Acceptance Criteria: The event cannot be created if the end date is earlier than the start date."""
    with pytest.raises(ValueError, match="End date can't be earlier than start date"):
        Event(
            event_name="Bad event",
            description="An event with end date earlier than start date.",
            start_date=date(2077, 12, 2),
            end_date=date(2077, 10, 1),
            location="Loc",
            max_capacity=100,
        )


def test_create_event_invalid_capacity():
    """US 1 Acceptance Criteria: The event cannot be created if the maximum capacity is less than or equal to zero."""
    with pytest.raises(ValueError, match="Max capacity must be greater than zero"):
        Event("Bad Event", "Desc", date(2077, 1, 1), date(2077, 1, 2), "Loc", 0)


def test_publish_event_success(valid_event, valid_ticket_category):
    """
    US 2 Acceptance Criteria:
    - An event with the status Draft can be changed to Published.
    - After the event is published, the system raises the domain event EventPublished.
    """
    valid_event.add_ticket_category(valid_ticket_category)
    valid_event.publish()

    assert valid_event.status == EventStatus.PUBLISHED
    assert any(isinstance(e, EventPublished) for e in valid_event._domain_events)


def test_publish_event_fails_no_categories(valid_event):
    """US 2 Acceptance Criteria: An event can only be published if it has at least one active ticket category."""
    with pytest.raises(
        ValueError, match="Event must have at least one ticket category"
    ):
        valid_event.publish()


def test_publish_event_fails_exceeds_capacity(valid_event, valid_ticket_category):
    """US 2 Acceptance Criteria: An event can only be published if the total ticket quota does not exceed the maximum event capacity."""
    valid_event.add_ticket_category(valid_ticket_category)

    # Artificially lower the max capacity to simulate the failure condition at publish time
    valid_event.max_capacity = 40

    with pytest.raises(ValueError, match="Total quota exceeds max capacity"):
        valid_event.publish()


def test_publish_event_fails_if_cancelled(valid_event, valid_ticket_category):
    """US 2 Acceptance Criteria: An event with the status Cancelled cannot be published."""
    valid_event.add_ticket_category(valid_ticket_category)
    valid_event.publish()
    valid_event.cancel()  # Status is now cancelled

    with pytest.raises(ValueError, match="Cannot publish a cancelled event"):
        valid_event.publish()


def test_cancel_event_success(valid_event, valid_ticket_category):
    """
    US 3 Acceptance Criteria:
    - An event with the status Published can be cancelled.
    - After the event is cancelled, the system raises the domain event EventCancelled.
    """
    valid_event.add_ticket_category(valid_ticket_category)
    valid_event.publish()
    valid_event.cancel()

    assert valid_event.status == EventStatus.CANCELLED
    assert any(isinstance(e, EventCancelled) for e in valid_event._domain_events)


def test_cancel_event_fails_if_completed(valid_event, valid_ticket_category):
    """US 3 Acceptance Criteria: An event with the status Completed cannot be cancelled."""
    valid_event.add_ticket_category(valid_ticket_category)
    valid_event.publish()
    valid_event.status = EventStatus.COMPLETED

    with pytest.raises(ValueError, match="Cannot cancel a completed event"):
        valid_event.cancel()
