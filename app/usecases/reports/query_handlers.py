from collections import Counter
from decimal import Decimal

from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.value_objects.booking_status import BookingStatus
from app.usecases.reports.dtos import (
    BookingReportDTO,
    EventSalesReportDTO,
    TicketCategorySalesDTO,
)
from app.usecases.reports.queries import ViewEventSalesReportQuery


class ViewEventSalesReportQueryHandler:
    def __init__(
        self, event_repository: EventRepository, booking_repository: BookingRepository
    ):
        self._event_repository = event_repository
        self._booking_repository = booking_repository

    def handle(self, query: ViewEventSalesReportQuery):
        event = self._event_repository.get_by_id(query.event_id)

        if not event:
            return None

        bookings = self._booking_repository.list_by_event(query.event_id)

        if not bookings:
            return None

        status_counter = Counter(b.status for b in bookings)
        total_revenue = sum(
            (
                b.total_price().amount
                for b in bookings
                if b.status == BookingStatus.PAID
            ),
            Decimal("0"),
        )

        return EventSalesReportDTO(
            name=event.name,
            ticket_categories=[
                TicketCategorySalesDTO(
                    name=tc.name,
                    price=tc.price.amount,
                    quota_sold=tc.quota_sold(),
                )
                for tc in event.get_ticket_categories
            ],
            bookings=[
                BookingReportDTO(
                    status=status.value,
                    total_bookings=count,
                    total_revenue=total_revenue
                    if status == BookingStatus.PAID
                    else Decimal("0"),
                )
                for status, count in status_counter.items()
            ],
        )
