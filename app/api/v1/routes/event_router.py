from datetime import date

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette.exceptions import HTTPException

from app.api.v1.schemas.event_schema import (
    CreateEventSchema,
    CreateTicketCategorySchema,
)
from app.application.usecases.event.commands import (
    CancelEventCommand,
    CreateEventCommand,
    CreateTicketCategoryCommand,
    DisableTicketCategoryCommand,
    PublishEventCommand,
)
from app.application.usecases.event.queries import (
    GetAllAvailableEventsQuery,
    GetEventDetailsQuery,
)
from app.application.usecases.reports.queries import (
    ViewEventParticipantsQuery,
    ViewEventSalesReportQuery,
)
from app.core.dependencies import (
    get_available_events_handler,
    get_cancel_event_handler,
    get_create_event_handler,
    get_create_ticket_category_handler,
    get_disable_ticket_category_handler,
    get_event_details_handler,
    get_participants_handler,
    get_publish_event_handler,
    get_sales_report_handler,
)
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.user_id import UserId

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", status_code=201)
def create_event(body: CreateEventSchema, handler=Depends(get_create_event_handler)):
    command = CreateEventCommand(
        event_name=body.event_name,
        description=body.description,
        start_date=body.start_date,
        end_date=body.end_date,
        location=body.location,
        max_capacity=body.max_capacity,
        event_organizer=UserId("dummy-organizer-id"),
    )

    try:
        event_id = handler.handle(command)
        return {"message": "Event created successfully", "event_id": event_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{event_id}/publish", status_code=200)
def publish_event(event_id: str, handler=Depends(get_publish_event_handler)):
    command = PublishEventCommand(event_id=EventId(event_id))
    try:
        handler.handle(command)
        return {"message": "Event published successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{event_id}/cancel", status_code=200)
def cancel_event(event_id: str, handler=Depends(get_cancel_event_handler)):
    command = CancelEventCommand(event_id=EventId(event_id))
    try:
        handler.handle(command)
        return {"message": "Event cancelled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{event_id}/categories", status_code=200)
def create_ticket_category(
    event_id: str,
    body: CreateTicketCategorySchema,
    handler=Depends(get_create_ticket_category_handler),
):
    command = CreateTicketCategoryCommand(
        event_id=EventId(event_id),
        category_name=body.category_name,
        price=body.price,
        quota=body.quota,
        sales_start_date=body.sales_start_date,
        sales_end_date=body.sales_end_date,
    )
    try:
        handler.handle(command)
        return {"message": "Ticket category created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{event_id}/categories/{category_id}/", status_code=200)
def disable_ticket_category(
    event_id: str,
    category_id: str,
    handler=Depends(get_disable_ticket_category_handler),
):
    command = DisableTicketCategoryCommand(
        event_id=EventId(event_id), category_id=TicketCategoryId(category_id)
    )
    try:
        handler.handle(command)
        return {"message": "Ticket category disabled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", status_code=200)
def get_available_events(
    start_date: date | None = None,
    end_date: date | None = None,
    location: str | None = None,
    handler=Depends(get_available_events_handler),
):
    query = GetAllAvailableEventsQuery(
        start_date=start_date, end_date=end_date, location=location
    )
    return handler.handle(query)


@router.get("/{event_id}/", status_code=200)
def get_event_details(
    event_id: str,
    handler=Depends(get_event_details_handler),
):
    query = GetEventDetailsQuery(event_id=EventId(event_id))
    result = handler.handle(query)

    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return result


@router.get("/{event_id}/report", status_code=200)
def get_event_report(
    event_id: str,
    handler=Depends(get_sales_report_handler),
):
    query = ViewEventSalesReportQuery(event_id=EventId(event_id))
    result = handler.handle(query)

    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return result


@router.get("/{event_id}/participants", status_code=200)
def get_event_participants(
    event_id: str,
    handler=Depends(get_participants_handler),
):
    query = ViewEventParticipantsQuery(event_id=EventId(event_id))
    return handler.handle(query)
