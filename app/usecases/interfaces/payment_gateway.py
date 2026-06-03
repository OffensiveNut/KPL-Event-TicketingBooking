from abc import ABC, abstractmethod

from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.money import Money


class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, booking_id: BookingId, amount: Money) -> bool:
        """Process a payment for a booking. Returns True if successful."""
