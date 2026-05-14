from enum import Enum


class BookingStatus(Enum):
    PENDING = "PendingPayment"
    EXPIRED = "Expired"
    PAID = "Paid"
    REFUNDED = "Refunded"
