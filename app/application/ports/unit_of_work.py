from abc import ABC, abstractmethod
from typing import Any

from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.repositories.refund_repository import RefundRepository


class UnitOfWork(ABC):
    events: EventRepository
    bookings: BookingRepository
    refunds: RefundRepository

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        """Commit the underlying database transaction."""

    @abstractmethod
    def rollback(self) -> None:
        """Rollback the underlying database transaction."""
