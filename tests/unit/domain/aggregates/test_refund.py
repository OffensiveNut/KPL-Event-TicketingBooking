"""US 16, 17: Refund approval and rejection rules."""
from decimal import Decimal

import pytest

from app.domain.aggregates.refund import Refund
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.money import Money


class TestRefundApproveInvalidStatus:
    def test_approve_already_approved_refund_raises_error(self):
        refund = Refund(booking_id=BookingId("book-1"), amount=Money(Decimal("100")))
        refund.approve()
        with pytest.raises(ValueError, match="not requested"):
            refund.approve()

    def test_approve_rejected_refund_raises_error(self):
        refund = Refund(booking_id=BookingId("book-1"), amount=Money(Decimal("100")))
        refund.reject(rejection_reason="Not eligible")
        with pytest.raises(ValueError, match="not requested"):
            refund.approve()

    def test_approve_paid_out_refund_raises_error(self):
        refund = Refund(booking_id=BookingId("book-1"), amount=Money(Decimal("100")))
        refund.approve()
        refund.paid_out(payment_reference="REF-001")
        with pytest.raises(ValueError, match="not requested"):
            refund.approve()


class TestRefundRejectReason:
    def test_reject_with_empty_reason_raises_error(self):
        refund = Refund(booking_id=BookingId("book-1"), amount=Money(Decimal("100")))
        with pytest.raises(ValueError, match="cannot be empty"):
            refund.reject(rejection_reason="")

    def test_reject_with_whitespace_reason_raises_error(self):
        refund = Refund(booking_id=BookingId("book-1"), amount=Money(Decimal("100")))
        with pytest.raises(ValueError, match="cannot be empty"):
            refund.reject(rejection_reason="   ")
