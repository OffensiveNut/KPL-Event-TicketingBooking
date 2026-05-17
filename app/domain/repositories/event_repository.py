from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from app.domain.aggregates.event import Event
from app.domain.value_objects.event_id import EventId


class EventRepository(ABC):
    @abstractmethod
    def save(self, event: Event) -> None:
        """Persist a new or existing event aggregate."""

    @abstractmethod
    def get_by_id(self, event_id: EventId) -> Event | None:
        """Return an event aggregate by its id, or None if not found."""

    @abstractmethod
    def list_published(
        self,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
        location: str | None = None,
    ) -> list[Event]:
        """Return published events with optional date/location filters."""
