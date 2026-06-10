from app.domain.repositories.booking_repository import BookingRepository
from app.domain.value_objects.booking_status import BookingStatus
from app.application.usecases.booking.dtos import BookingTotalPriceDTO, TicketSummaryDTO
from app.application.usecases.booking.queries import (
    CalculateBookingQuery,
    ViewPurchasedTicketsQuery,
)


class CalculateBookingQueryHandler:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def handle(self, query: CalculateBookingQuery) -> BookingTotalPriceDTO:
        booking = self.booking_repository.get_by_id(query.booking_id)
        if not booking:
            raise ValueError(f"Booking with id {query.booking_id} not found")

        booking_total_price = booking.total_price()
        return BookingTotalPriceDTO(total_price=booking_total_price.amount)


class ViewPurchasedTicketsQueryHandler:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def handle(self, query: ViewPurchasedTicketsQuery) -> list[TicketSummaryDTO]:
        booking = self.booking_repository.get_by_id(query.booking_id)
        if not booking:
            raise ValueError(f"Booking with id {query.booking_id} not found")
        if booking.status != BookingStatus.PAID:
            raise ValueError("Only paid bookings can view purchased tickets")

        return [
            TicketSummaryDTO(
                ticket_id=ticket.id.value,
                ticket_code=ticket.ticket_code.value,
                event_id=ticket.event_id.value,
                status=ticket.status.value,
            )
            for ticket in booking.tickets
        ]
