import uuid
from datetime import datetime, timedelta

from app.domain.entities.ticket import Ticket
from app.domain.events.booking_expired import BookingExpired
from app.domain.events.booking_paid import BookingPaid
from app.domain.events.ticket_reserved import TicketReserved
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.booking_status import BookingStatus
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.money import Money
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.user_id import UserId


class Booking:
    def __init__(
        self,
        ticket_category_id: TicketCategoryId,
        event_id: EventId,
        ticket_quantity: int,
        ticket_price: Money,
        service_fee: Money,
        customer_id: UserId,
    ) -> None:
        if ticket_quantity <= 0:
            raise ValueError("Ticket quantity must be greater than 0")

        self.id = BookingId(str(uuid.uuid4()))
        self.customer_id = customer_id
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.status = BookingStatus.PENDING
        self.payment_deadline = datetime.now() + timedelta(minutes=15)
        self.ticket_quantity = ticket_quantity
        self.ticket_price = ticket_price
        self.service_fee = service_fee

        self.tickets: list[Ticket] = []

        self._domain_events: list = []
        self._domain_events.append(
            TicketReserved(
                booking_id=self.id,
                event_id=event_id,
                ticket_category_id=ticket_category_id,
            )
        )

    def total_price(self) -> Money:
        total = self.ticket_price.multiply(self.ticket_quantity).add(self.service_fee)
        return total

    def pay(self, payment: Money) -> None:
        if self.status != BookingStatus.PENDING:
            raise ValueError("Only pending bookings can be paid")
        if self.payment_deadline < datetime.now():
            raise ValueError("Payment deadline has passed")
        if payment.amount != self.total_price().amount:
            raise ValueError("Payment amount must match total price")

        self.status = BookingStatus.PAID

        for _ in range(self.ticket_quantity):
            self.tickets.append(Ticket(booking_id=self.id, event_id=self.event_id))

        self._domain_events.append(
            BookingPaid(
                booking_id=self.id,
            )
        )

    def expire(self) -> None:
        if self.status != BookingStatus.PENDING:
            raise ValueError("Only pending bookings can be expired")

        self.status = BookingStatus.EXPIRED
        self._domain_events.append(
            BookingExpired(
                booking_id=self.id,
            )
        )
