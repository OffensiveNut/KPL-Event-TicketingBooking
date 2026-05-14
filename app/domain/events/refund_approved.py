from dataclasses import dataclass

from app.domain.value_objects.refund_id import RefundId


@dataclass
class RefundApproved:
    refund_id: RefundId
