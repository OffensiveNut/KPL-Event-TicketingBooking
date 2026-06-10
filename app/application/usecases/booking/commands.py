from dataclasses import dataclass
from decimal import Decimal

from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.ticket_id import TicketId
from app.domain.value_objects.user_id import UserId


@dataclass
class CreateBookingCommand:
    event_id: EventId
    ticket_category_id: TicketCategoryId
    ticket_category_name: str
    ticket_quantity: int
    price: Decimal
    service_fee: Decimal
    customer_id: UserId
    customer_name: str


@dataclass
class PayBookingCommand:
    booking_id: BookingId
    pay_amount: Decimal


@dataclass
class ExpireBookingCommand:
    booking_id: BookingId


@dataclass
class CheckinTicketCommand:
    event_id: EventId
    ticket_id: TicketId
    ticket_code: TicketCode
