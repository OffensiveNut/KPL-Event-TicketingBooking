from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.domain.aggregates.booking import Booking
from app.domain.entities.ticket import Ticket
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.booking_status import BookingStatus
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.money import Money
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.ticket_id import TicketId
from app.domain.value_objects.ticket_status import TicketStatus
from app.domain.value_objects.user_id import UserId
from app.infrastructure.models.booking_model import BookingModel, TicketModel


class SqlAlchemyBookingRepository(BookingRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, booking: Booking) -> None:
        model = self._to_model(booking)
        self._session.merge(model)

    def get_by_id(self, booking_id: BookingId) -> Booking | None:
        stmt = (
            select(BookingModel)
            .options(selectinload(BookingModel.tickets))
            .where(BookingModel.id == booking_id.value)
        )
        model = self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_domain(model)

    def get_active_by_customer_event(
        self, customer_id: UserId, event_id: EventId
    ) -> Booking | None:
        stmt = (
            select(BookingModel)
            .options(selectinload(BookingModel.tickets))
            .where(BookingModel.customer_id == customer_id.value)
            .where(BookingModel.event_id == event_id.value)
            .where(
                BookingModel.status.in_(
                    [BookingStatus.PENDING.value, BookingStatus.PAID.value]
                )
            )
        )
        model = self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_domain(model)

    def list_by_event(self, event_id: EventId) -> list[Booking]:
        stmt = (
            select(BookingModel)
            .options(selectinload(BookingModel.tickets))
            .where(BookingModel.event_id == event_id.value)
        )
        models = self._session.scalars(stmt).all()
        return [self._to_domain(model) for model in models]

    def _to_model(self, booking: Booking) -> BookingModel:
        tickets = [
            TicketModel(
                id=ticket.id.value,
                booking_id=booking.id.value,
                event_id=booking.event_id.value,
                ticket_code=ticket.ticket_code.value,
                status=ticket.status.value,
            )
            for ticket in booking.tickets
        ]

        return BookingModel(
            id=booking.id.value,
            event_id=booking.event_id.value,
            customer_id=booking.customer_id.value,
            ticket_category_id=booking.ticket_category_id.value,
            status=booking.status.value,
            payment_deadline=booking.payment_deadline,
            ticket_quantity=booking.ticket_quantity,
            ticket_price=booking.ticket_price.amount,
            service_fee=booking.service_fee.amount,
            tickets=tickets,
        )

    def _to_domain(self, model: BookingModel) -> Booking:
        booking = Booking(
            ticket_category_id=TicketCategoryId(model.ticket_category_id),
            event_id=EventId(model.event_id),
            ticket_quantity=model.ticket_quantity,
            ticket_price=Money(model.ticket_price),
            service_fee=Money(model.service_fee),
            customer_id=UserId(model.customer_id),
        )
        booking.id = BookingId(model.id)
        booking.status = BookingStatus(model.status)
        booking.payment_deadline = model.payment_deadline
        booking.tickets = [self._to_domain_ticket(ticket) for ticket in model.tickets]
        booking._domain_events = []
        return booking

    def _to_domain_ticket(self, model: TicketModel) -> Ticket:
        ticket = Ticket(
            booking_id=BookingId(model.booking_id),
            event_id=EventId(model.event_id),
        )
        ticket.id = TicketId(model.id)
        ticket.ticket_code = TicketCode(model.ticket_code)
        ticket.status = TicketStatus(model.status)
        return ticket
