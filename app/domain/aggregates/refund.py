import uuid

from app.domain.events.refund_approved import RefundApproved
from app.domain.events.refund_paid_out import RefundPaidOut
from app.domain.events.refund_rejected import RefundRejected
from app.domain.events.refund_requested import RefundRequested
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.money import Money
from app.domain.value_objects.refund_id import RefundId
from app.domain.value_objects.refund_status import RefundStatus


class Refund:
    def __init__(self, booking_id: BookingId, amount: Money):
        self.id = RefundId(str(uuid.uuid4()))
        self.booking_id = booking_id
        self.amount = amount
        self.status = RefundStatus.REQUESTED

        self._domain_events: list = []
        self._domain_events.append(RefundRequested(refund_id=self.id))

    def approve(self) -> None:
        if self.status != RefundStatus.REQUESTED:
            raise ValueError("Cannot approve a refund that is not requested")

        self.status = RefundStatus.APPROVED
        self._domain_events.append(RefundApproved(refund_id=self.id))

    def reject(self, rejection_reason: str) -> None:
        if self.status != RefundStatus.REQUESTED:
            raise ValueError("Cannot reject a refund that is not requested")

        self.status = RefundStatus.REJECTED
        self.rejection_reason = rejection_reason
        self._domain_events.append(RefundRejected(refund_id=self.id))

    def paid_out(self) -> None:
        if self.status != RefundStatus.APPROVED:
            raise ValueError("Cannot mark a refund as paid out that is not approved")

        self.status = RefundStatus.PAIDOUT
        self._domain_events.append(RefundPaidOut(refund_id=self.id))
