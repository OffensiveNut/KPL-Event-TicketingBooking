from dataclasses import dataclass

from app.domain.value_objects.booking_id import BookingId


@dataclass
class BookingPaid:
    booking_id: BookingId
