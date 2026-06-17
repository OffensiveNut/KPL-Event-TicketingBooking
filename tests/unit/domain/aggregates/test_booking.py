"""US 8, 10, 11: Booking creation, payment, and expiry rules."""
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from app.domain.aggregates.booking import Booking
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.money import Money
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.user_id import UserId


class TestBookingZeroQuantity:
    def test_zero_quantity_raises_error(self):
        with pytest.raises(ValueError, match="greater than 0"):
            Booking(
                ticket_category_id=TicketCategoryId("cat-1"),
                ticket_category_name="Regular",
                event_id=EventId("event-1"),
                ticket_quantity=0,
                ticket_price=Money(Decimal("100")),
                service_fee=Money(Decimal("0")),
                customer_id=UserId("cust-1"),
                customer_name="Customer",
            )


class TestBookingPayAfterDeadline:
    def test_pay_after_deadline_raises_error(self, valid_booking):
        valid_booking.payment_deadline = datetime.now() - timedelta(minutes=1)
        with pytest.raises(ValueError, match="Payment deadline has passed"):
            valid_booking.pay(Money(Decimal("200")))


class TestBookingPayWrongAmount:
    def test_pay_with_incorrect_amount_raises_error(self, valid_booking):
        valid_booking.payment_deadline = datetime.now() + timedelta(hours=1)
        with pytest.raises(ValueError, match="Payment amount must match"):
            valid_booking.pay(Money(Decimal("50")))


class TestPaidBookingExpire:
    def test_paid_booking_cannot_expire(self, valid_booking):
        valid_booking.payment_deadline = datetime.now() + timedelta(hours=1)
        valid_booking.pay(Money(Decimal("200")))
        with pytest.raises(ValueError, match="Only pending bookings can be expired"):
            valid_booking.expire()
