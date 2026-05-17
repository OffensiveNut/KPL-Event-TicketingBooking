from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.aggregates.refund import Refund
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.refund_id import RefundId


class RefundRepository(ABC):
    @abstractmethod
    def save(self, refund: Refund) -> None:
        """Persist a new or existing refund aggregate."""

    @abstractmethod
    def get_by_id(self, refund_id: RefundId) -> Refund | None:
        """Return a refund aggregate by its id, or None if not found."""

    @abstractmethod
    def get_by_booking_id(self, booking_id: BookingId) -> Refund | None:
        """Return a refund for a booking, or None if not found."""
