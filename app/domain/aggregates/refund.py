import uuid

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

