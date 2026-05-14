from dataclasses import dataclass

from app.domain.value_objects.refund_id import RefundId


@dataclass
class RefundPaidOut:
    refund_id: RefundId
