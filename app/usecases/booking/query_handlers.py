from app.domain.repositories.booking_repository import BookingRepository
from app.usecases.booking.dtos import BookingTotalPrice
from app.usecases.booking.queries import CalculateBookingQuery


class CalculateBookingQueryHandler:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def handle(self, query: CalculateBookingQuery) -> BookingTotalPrice:
        booking = self.booking_repository.get_by_id(query.booking_id)
        if not booking:
            raise ValueError(f"Booking with id {query.booking_id} not found")

        booking_total_price = booking.total_price()
        return BookingTotalPrice(total_price=booking_total_price.amount)
