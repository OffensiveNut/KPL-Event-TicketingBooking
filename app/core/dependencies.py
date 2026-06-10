from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.usecases.event.command_handlers import (
    CancelEventCommandHandler,
    CreateEventCommandHandler,
    CreateTicketCategoryCommandHandler,
    DisableTicketCategoryCommandHandler,
    PublishEventCommandHandler,
)
from app.application.usecases.event.query_handlers import (
    GetAllAvailableEventsQueryHandler,
    GetEventDetailsQueryHandler,
)
from app.application.usecases.reports.query_handlers import (
    ViewEventParticipantsQueryHandler,
    ViewEventSalesReportQueryHandler,
)
from app.infrastructure.database import get_db
from app.infrastructure.repositories.booking_repo import SqlAlchemyBookingRepository
from app.infrastructure.repositories.event_repo import SqlAlchemyEventRepository


def get_event_repository(db: Session = Depends(get_db)) -> SqlAlchemyEventRepository:
    return SqlAlchemyEventRepository(db)


def get_booking_repository(db: Session = Depends(get_db)) -> SqlAlchemyBookingRepository:
    return SqlAlchemyBookingRepository(db)


def get_create_event_handler(
    event_repo=Depends(get_event_repository),
) -> CreateEventCommandHandler:
    return CreateEventCommandHandler(event_repo)


def get_publish_event_handler(
    event_repo=Depends(get_event_repository),
) -> PublishEventCommandHandler:
    return PublishEventCommandHandler(event_repo)


def get_cancel_event_handler(
    event_repo=Depends(get_event_repository),
) -> CancelEventCommandHandler:
    return CancelEventCommandHandler(event_repo)


def get_create_ticket_category_handler(
    event_repo=Depends(get_event_repository),
) -> CreateTicketCategoryCommandHandler:
    return CreateTicketCategoryCommandHandler(event_repo)


def get_disable_ticket_category_handler(
    event_repo=Depends(get_event_repository),
) -> DisableTicketCategoryCommandHandler:
    return DisableTicketCategoryCommandHandler(event_repo)


def get_available_events_handler(
    event_repo=Depends(get_event_repository),
) -> GetAllAvailableEventsQueryHandler:
    return GetAllAvailableEventsQueryHandler(event_repo)


def get_event_details_handler(
    event_repo=Depends(get_event_repository),
) -> GetEventDetailsQueryHandler:
    return GetEventDetailsQueryHandler(event_repo)


def get_sales_report_handler(
    event_repo=Depends(get_event_repository),
    booking_repo=Depends(get_booking_repository),
) -> ViewEventSalesReportQueryHandler:
    return ViewEventSalesReportQueryHandler(event_repo, booking_repo)


def get_participants_handler(
    booking_repo=Depends(get_booking_repository),
) -> ViewEventParticipantsQueryHandler:
    return ViewEventParticipantsQueryHandler(booking_repo)
