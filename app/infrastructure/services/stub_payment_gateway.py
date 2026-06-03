import logging

from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.money import Money
from app.usecases.interfaces.payment_gateway import PaymentGateway

logger = logging.getLogger(__name__)


class StubPaymentGateway(PaymentGateway):
    def process_payment(self, booking_id: BookingId, amount: Money) -> bool:
        # dummy implementation
        logger.info(
            f"[StubPaymentGateway] Successfully processed payment of {amount.amount} "
            f"for booking {booking_id.value}"
        )
        return True
