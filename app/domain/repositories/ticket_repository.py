from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.ticket import Ticket
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.ticket_id import TicketId


class TicketRepository(ABC):
    @abstractmethod
    def save(self, ticket: Ticket) -> None:
        """Persist a new or existing ticket entity."""

    @abstractmethod
    def get_by_id(self, ticket_id: TicketId) -> Ticket | None:
        """Return a ticket by its id, or None if not found."""

    @abstractmethod
    def get_by_code(self, ticket_code: TicketCode) -> Ticket | None:
        """Return a ticket by its unique ticket code, or None if not found."""

    @abstractmethod
    def list_by_booking(self, booking_id: BookingId) -> list[Ticket]:
        """Return all tickets for a given booking."""
