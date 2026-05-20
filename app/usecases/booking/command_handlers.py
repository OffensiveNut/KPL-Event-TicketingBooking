from app.domain.aggregates.booking import Booking
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.value_objects.event_status import EventStatus
from app.domain.value_objects.money import Money
from app.usecases.booking.commands import (
    CreateBookingCommand,
    ExpireBookingCommand,
    PayBookingCommand,
)


class CreateBookingCommandHandler:
    def __init__(
        self, booking_repository: BookingRepository, event_repository: EventRepository
    ):
        self.booking_repository = booking_repository
        self.event_repository = event_repository

    def handle(self, command: CreateBookingCommand) -> str:
        event = self.event_repository.get_by_id(command.event_id)

        if not event:
            raise ValueError(f"Event with id {command.event_id} not found")
        if event.status != EventStatus.PUBLISHED:
            raise ValueError("Only published events can be booked")

        ticket_category = event.get_ticket_category_by_id(command.ticket_category_id)

        if not ticket_category:
            raise ValueError(
                f"Ticket category with id {command.ticket_category_id} not found"
            )
        if not ticket_category.is_active:
            raise ValueError("Ticket category is not active")
        if not ticket_category.sales_period.is_active():
            raise ValueError("Ticket category is not active")
        if ticket_category.remaining_quota < command.ticket_quantity:
            raise ValueError("Not enough quota available")

        customer_booking = self.booking_repository.get_active_by_customer_event(
            command.customer_id, command.event_id
        )

        if customer_booking:
            raise ValueError("Customer already has an active booking for this event")

        booking = Booking(
            event_id=command.event_id,
            ticket_category_id=command.ticket_category_id,
            ticket_quantity=command.ticket_quantity,
            ticket_price=Money(command.price),
            service_fee=Money(command.service_fee),
            customer_id=command.customer_id,
        )

        ticket_category.reserve(command.ticket_quantity)
        self.booking_repository.save(booking)
        self.event_repository.save(event)

        return booking.id.value


class PayBookingCommandHandler:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def handle(self, command: PayBookingCommand) -> None:
        booking = self.booking_repository.get_by_id(command.booking_id)
        if not booking:
            raise ValueError("Booking not found")

        booking.pay(Money(command.pay_amount))
        self.booking_repository.save(booking)


class ExpireBookingCommandHandler:
    def __init__(
        self, booking_repository: BookingRepository, event_repository: EventRepository
    ):
        self.booking_repository = booking_repository
        self.event_repository = event_repository

    def handle(self, command: ExpireBookingCommand) -> None:
        booking = self.booking_repository.get_by_id(command.booking_id)
        if not booking:
            raise ValueError("Booking not found")

        event = self.event_repository.get_by_id(booking.event_id)
        if not event:
            raise ValueError("Event not found")

        ticket_category = event.get_ticket_category_by_id(booking.ticket_category_id)
        if not ticket_category:
            raise ValueError("Ticket category not found")

        booking.expire()
        ticket_category.release(booking.ticket_quantity)

        self.event_repository.save(event)
        self.booking_repository.save(booking)
