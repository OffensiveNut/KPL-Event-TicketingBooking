from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.ticket import Ticket
from app.domain.repositories.ticket_repository import TicketRepository
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.ticket_id import TicketId
from app.domain.value_objects.ticket_status import TicketStatus
from app.infrastructure.models.booking_model import TicketModel


class SqlAlchemyTicketRepository(TicketRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, ticket: Ticket) -> None:
        model = TicketModel(
            id=ticket.id.value,
            booking_id=ticket.booking_id.value,
            event_id=ticket.event_id.value,
            ticket_code=ticket.ticket_code.value,
            status=ticket.status.value,
        )
        self._session.merge(model)

    def get_by_id(self, ticket_id: TicketId) -> Ticket | None:
        model = self._session.get(TicketModel, ticket_id.value)
        if model is None:
            return None
        return self._to_domain(model)

    def get_by_code(self, ticket_code: TicketCode) -> Ticket | None:
        stmt = select(TicketModel).where(TicketModel.ticket_code == ticket_code.value)
        model = self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_domain(model)

    def list_by_booking(self, booking_id: BookingId) -> list[Ticket]:
        stmt = select(TicketModel).where(TicketModel.booking_id == booking_id.value)
        models = self._session.scalars(stmt).all()
        return [self._to_domain(model) for model in models]

    def _to_domain(self, model: TicketModel) -> Ticket:
        ticket = Ticket(
            booking_id=BookingId(model.booking_id),
            event_id=EventId(model.event_id),
        )
        ticket.id = TicketId(model.id)
        ticket.ticket_code = TicketCode(model.ticket_code)
        ticket.status = TicketStatus(model.status)
        return ticket
