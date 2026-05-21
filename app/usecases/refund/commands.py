from dataclasses import dataclass

from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.refund_id import RefundId


@dataclass
class RequestRefundCommand:
    booking_id: BookingId
    event_id: EventId


@dataclass
class ApproveRefundCommand:
    refund_id: RefundId
