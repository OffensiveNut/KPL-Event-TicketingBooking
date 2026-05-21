from datetime import date

from app.domain.aggregates.refund import Refund
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.value_objects.booking_status import BookingStatus
from app.domain.value_objects.event_status import EventStatus
from app.domain.value_objects.ticket_status import TicketStatus
from app.usecases.refund.commands import ApproveRefundCommand, RequestRefundCommand


class RequestRefundCommandHandler:
    def __init__(
        self,
        booking_repository: BookingRepository,
        event_repository: EventRepository,
        refund_repository: RefundRepository,
    ):
        self._booking_repository = booking_repository
        self._event_repository = event_repository
        self._refund_repository = refund_repository

    def handle(self, command: RequestRefundCommand) -> None:
        booking = self._booking_repository.get_by_id(command.booking_id)
        event = self._event_repository.get_by_id(command.event_id)

        if booking is None:
            raise ValueError("Booking not found")
        if event is None:
            raise ValueError("Event not found")
        if booking.status != BookingStatus.PAID:
            raise ValueError("Booking is not paid")

        for ticket in booking.tickets:
            if ticket.status == TicketStatus.CHECKED_IN:
                raise ValueError("Cannot refund a checked-in ticket")

        if event.status != EventStatus.CANCELLED:
            if date.today() >= event.date.start_date:
                raise ValueError("Cannot refund before the event starts")

        refund = Refund(booking_id=booking.id, amount=booking.total_price())
        self._refund_repository.save(refund)


class ApproveRefundCommandHandler:
    def __init__(
        self,
        refund_repository: RefundRepository,
        booking_repository: BookingRepository,
    ):
        self._refund_repository = refund_repository
        self._booking_repository = booking_repository

    def handle(self, command: ApproveRefundCommand) -> None:
        refund = self._refund_repository.get_by_id(command.refund_id)

        if refund is None:
            raise ValueError("Refund not found")

        booking = self._booking_repository.get_by_id(refund.booking_id)

        if booking is None:
            raise ValueError("Booking not found")

        refund.approve()
        
        for ticket in booking.tickets:
            ticket.status = TicketStatus.CANCELLED
        booking.status = BookingStatus.REFUNDED

        self._booking_repository.save(booking)
        self._refund_repository.save(refund)
