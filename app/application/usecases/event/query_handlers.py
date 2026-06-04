from app.domain.entities.ticket_category import TicketCategory
from app.domain.repositories.event_repository import EventRepository
from app.usecases.event.dtos import EventDetailsDTO, EventSummaryDTO, TicketCategoryDTO
from app.usecases.event.queries import GetAllAvailableEventsQuery, GetEventDetailsQuery


class GetAllAvailableEventsQueryHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, query: GetAllAvailableEventsQuery) -> list[EventSummaryDTO]:
        events = self.event_repository.list_published(
            start_date=query.start_date,
            end_date=query.end_date,
            location=query.location,
        )

        return [
            EventSummaryDTO(
                id=event.id.value,
                name=event.name,
                start_date=event.date.start_date,
                end_date=event.date.end_date,
                location=event.location,
            )
            for event in events
        ]


class GetEventDetailsQueryHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, query: GetEventDetailsQuery) -> EventDetailsDTO | None:
        event = self.event_repository.get_by_id(query.event_id)

        if event is None:
            return None
        return EventDetailsDTO(
            id=event.id.value,
            name=event.name,
            start_date=event.date.start_date,
            end_date=event.date.end_date,
            location=event.location,
            description=event.description,
            organizer_id=event.event_organizer.value,
            ticket_categories=[
                TicketCategoryDTO(
                    id=tc.id.value,
                    name=tc.name,
                    price=tc.price.amount,
                    quota=tc.quota,
                    remaining_quota=tc.remaining_quota,
                    status=self._get_category_status(tc),
                )
                for tc in event.get_ticket_categories
                if tc.is_active
            ],
        )

    def _get_category_status(self, tc: TicketCategory) -> str:
        if tc.remaining_quota == 0:
            return "Sold Out"
        if tc.sales_period.is_coming_soon():
            return "Coming Soon"
        if tc.sales_period.is_ended():
            return "Ended"
        return "Available"
