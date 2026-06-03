from abc import ABC, abstractmethod

from app.domain.value_objects.money import Money
from app.domain.value_objects.refund_id import RefundId


class RefundPaymentService(ABC):
    @abstractmethod
    def process_refund_payout(self, refund_id: RefundId, amount: Money) -> str:
        """Process a refund payout to a customer. Returns a payment reference string."""
