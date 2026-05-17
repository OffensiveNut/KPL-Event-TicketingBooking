from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.aggregates.booking import Booking
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.user_id import UserId


class BookingRepository(ABC):
    @abstractmethod
    def save(self, booking: Booking) -> None:
        """Persist a new or existing booking aggregate."""

    @abstractmethod
    def get_by_id(self, booking_id: BookingId) -> Booking | None:
        """Return a booking aggregate by its id, or None if not found."""

    @abstractmethod
    def get_active_by_customer_event(
        self, customer_id: UserId, event_id: EventId
    ) -> Booking | None:
        """Return active booking (Pending/Paid) for a customer/event, if any."""

    @abstractmethod
    def list_by_event(self, event_id: EventId) -> list[Booking]:
        """Return all bookings for a given event."""
