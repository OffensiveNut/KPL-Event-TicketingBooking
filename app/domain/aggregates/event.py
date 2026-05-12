import uuid
from datetime import date

from app.domain.entities.ticket_category import TicketCategory
from app.domain.events.event_cancelled import EventCancelled
from app.domain.events.event_created import EventCreated
from app.domain.events.event_published import EventPublished
from app.domain.events.ticket_category_created import TicketCategoryCreated
from app.domain.events.ticket_category_disabled import TicketCategoryDisabled
from app.domain.value_objects.date_range import DateRange
from app.domain.value_objects.event_status import EventStatus


class Event:
    def __init__(
        self,
        event_name: str,
        description: str,
        start_date: date,
        end_date: date,
        location: str,
        max_capacity: int,
    ) -> None:
        if max_capacity <= 0:
            raise ValueError("Max capacity must be greater than zero")

        self.id = str(uuid.uuid4())
        self.name = event_name
        self.description = description
        self.date = DateRange(start_date, end_date)
        self.location = location
        self.max_capacity = max_capacity
        self.status = EventStatus.DRAFT

        self._domain_events: list = []
        self._domain_events.append(EventCreated(event_id=self.id, event_name=self.name))

        self._ticket_categories: list[TicketCategory] = []

    def _total_quota(self) -> int:
        return sum(tc.quota for tc in self._ticket_categories)

    def publish(self) -> None:
        if self.status == EventStatus.CANCELLED:
            raise ValueError("Cannot publish a cancelled event")
        if self.status != EventStatus.DRAFT:
            raise ValueError("Event must be in draft status to be published")
        if not any(tc.is_active for tc in self._ticket_categories):
            raise ValueError("Event must have at least one ticket category")
        if self._total_quota() > self.max_capacity:
            raise ValueError("Total quota exceeds max capacity")

        self.status = EventStatus.PUBLISHED
        self._domain_events.append(
            EventPublished(event_id=self.id, event_name=self.name)
        )

    def cancel(self) -> None:
        if self.status == EventStatus.COMPLETED:
            raise ValueError("Cannot cancel a completed event")
        if self.status != EventStatus.PUBLISHED:
            raise ValueError("Only published event can be cancelled")

        self.status = EventStatus.CANCELLED
        self._domain_events.append(
            EventCancelled(event_id=self.id, event_name=self.name)
        )

    def add_ticket_category(self, ticket_category: TicketCategory) -> None:
        if self._total_quota() + ticket_category.quota > self.max_capacity:
            raise ValueError("Total quota exceeds max capacity")
        if ticket_category.sales_period.end_date > self.date.start_date:
            raise ValueError("Sales period must end before or at the event start date")

        self._ticket_categories.append(ticket_category)
        self._domain_events.append(
            TicketCategoryCreated(
                event_id=self.id,
                category_id=ticket_category.id,
                name=ticket_category.name,
            )
        )

    def disable_ticket_category(self, category_id: str) -> None:
        category = next(
            (c for c in self._ticket_categories if c.id == category_id), None
        )
        if category is None:
            raise ValueError("Ticket category not found")
        if self.status == EventStatus.COMPLETED:
            raise ValueError("Cannot disable ticket category for a completed event")

        category.disable()
        self._domain_events.append(
            TicketCategoryDisabled(category_id=category_id, event_id=self.id)
        )
