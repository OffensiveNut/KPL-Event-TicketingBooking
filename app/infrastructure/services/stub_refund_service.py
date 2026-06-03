import logging
import uuid

from app.domain.value_objects.money import Money
from app.domain.value_objects.refund_id import RefundId
from app.usecases.interfaces.refund_service import RefundPaymentService

logger = logging.getLogger(__name__)


class StubRefundPaymentService(RefundPaymentService):
    def process_refund_payout(self, refund_id: RefundId, amount: Money) -> str:
        # dummy implementation
        payment_reference = f"REF-{uuid.uuid4().hex[:8].upper()}"

        logger.info(
            f"[StubRefundService] Processed refund payout of {amount.amount} "
            f"for refund {refund_id.value}. Reference: {payment_reference}"
        )
        return payment_reference
