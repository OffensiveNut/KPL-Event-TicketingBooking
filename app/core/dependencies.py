from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.usecases.booking.command_handlers import (
    CheckinTicketCommandHandler,
    CreateBookingCommandHandler,
    ExpireBookingCommandHandler,
    PayBookingCommandHandler,
)
from app.application.usecases.booking.query_handlers import (
    CalculateBookingQueryHandler,
    ViewPurchasedTicketsQueryHandler,
)
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
from app.infrastructure.SQLAlchemy.database import get_db
from app.infrastructure.SQLAlchemy.repositories.booking_repo import (
    SqlAlchemyBookingRepository,
)
from app.infrastructure.SQLAlchemy.repositories.event_repo import (
    SqlAlchemyEventRepository,
)


def get_event_repository(db: Session = Depends(get_db)) -> SqlAlchemyEventRepository:
    return SqlAlchemyEventRepository(db)


def get_booking_repository(
    db: Session = Depends(get_db),
) -> SqlAlchemyBookingRepository:
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


def get_create_booking_handler(
    booking_repo=Depends(get_booking_repository),
    event_repo=Depends(get_event_repository),
) -> CreateBookingCommandHandler:
    return CreateBookingCommandHandler(booking_repo, event_repo)


def get_pay_booking_handler(
    booking_repo=Depends(get_booking_repository),
) -> PayBookingCommandHandler:
    return PayBookingCommandHandler(booking_repo)


def get_expire_booking_handler(
    booking_repo=Depends(get_booking_repository),
    event_repo=Depends(get_event_repository),
) -> ExpireBookingCommandHandler:
    return ExpireBookingCommandHandler(booking_repo, event_repo)


def get_checkin_ticket_handler(
    booking_repo=Depends(get_booking_repository),
    event_repo=Depends(get_event_repository),
) -> CheckinTicketCommandHandler:
    return CheckinTicketCommandHandler(booking_repo, event_repo)


def get_view_purchased_tickets_handler(
    booking_repo=Depends(get_booking_repository),
) -> ViewPurchasedTicketsQueryHandler:
    return ViewPurchasedTicketsQueryHandler(booking_repo)


def get_calculate_booking_handler(
    booking_repo=Depends(get_booking_repository),
) -> CalculateBookingQueryHandler:
    return CalculateBookingQueryHandler(booking_repo)
