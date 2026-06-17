"""US 1, 2, 4: Event creation and publication rules."""
from datetime import date
from decimal import Decimal

import pytest

from app.domain.aggregates.event import Event
from app.domain.value_objects.user_id import UserId


class TestEventInvalidCapacity:
    def test_zero_capacity_raises_error(self):
        with pytest.raises(ValueError, match="Max capacity"):
            Event(
                event_name="Test", description="",
                start_date=date(2026, 7, 1), end_date=date(2026, 7, 2),
                location="", max_capacity=0,
                event_organizer=UserId("org-1"),
            )

    def test_negative_capacity_raises_error(self):
        with pytest.raises(ValueError, match="Max capacity"):
            Event(
                event_name="Test", description="",
                start_date=date(2026, 7, 1), end_date=date(2026, 7, 2),
                location="", max_capacity=-5,
                event_organizer=UserId("org-1"),
            )


class TestEventPublishWithoutCategory:
    def test_publish_without_ticket_categories_raises_error(self, valid_event):
        with pytest.raises(ValueError, match="at least one ticket category"):
            valid_event.publish()

    def test_publish_with_all_categories_disabled_raises_error(self, valid_event):
        valid_event.add_ticket_category("VIP", Decimal("200"), 50, date(2026, 6, 1), date(2026, 6, 30))
        for tc in valid_event._ticket_categories:
            tc.disable()
        with pytest.raises(ValueError, match="at least one ticket category"):
            valid_event.publish()


class TestTicketCategoryQuota:
    def test_add_category_exceeding_capacity_raises_error(self, valid_event):
        valid_event.add_ticket_category("Regular", Decimal("50"), 80, date(2026, 6, 1), date(2026, 6, 30))
        with pytest.raises(ValueError, match="quota exceeds max capacity"):
            valid_event.add_ticket_category("VIP", Decimal("100"), 30, date(2026, 6, 1), date(2026, 6, 30))
