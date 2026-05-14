from dataclasses import dataclass

from app.domain.value_objects.refund_id import RefundId


@dataclass
class RefundRequested:
    refund_id: RefundId
