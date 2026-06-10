from pyexpat.errors import codes

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from app.api.v1.schemas.booking_schema import (
    CheckinTicketSchema,
    CreateBookingSchema,
    PayBookingSchema,
)
from app.application.usecases.booking.commands import (
    CheckinTicketCommand,
    CreateBookingCommand,
    ExpireBookingCommand,
    PayBookingCommand,
)
from app.application.usecases.booking.queries import (
    CalculateBookingQuery,
    ViewPurchasedTicketsQuery,
)
from app.core.dependencies import (
    get_calculate_booking_handler,
    get_checkin_ticket_handler,
    get_create_booking_handler,
    get_expire_booking_handler,
    get_pay_booking_handler,
    get_view_purchased_tickets_handler,
)
from app.domain.aggregates import booking
from app.domain.value_objects import event_id
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.ticket_id import TicketId
from app.domain.value_objects.user_id import UserId

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", status_code=201)
def create_booking(
    body: CreateBookingSchema, handler=Depends(get_create_booking_handler)
):
    command = CreateBookingCommand(
        event_id=EventId(body.event_id),
        ticket_category_id=TicketCategoryId(body.ticket_category_id),
        ticket_category_name=body.ticket_category_name,
        ticket_quantity=body.ticket_quantity,
        price=body.price,
        service_fee=body.service_fee,
        customer_id=UserId("dummy-user-id"),
        customer_name="dummy-user-name",
    )

    try:
        booking_id = handler.handle(command)
        return {"booking_id": booking_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{booking_id}/pay", status_code=200)
def pay_booking(
    booking_id: str, body: PayBookingSchema, handler=Depends(get_pay_booking_handler)
):
    command = PayBookingCommand(
        booking_id=BookingId(booking_id), pay_amount=body.payment_amount
    )

    try:
        handler.handle(command)
        return {"message": "Booking paid successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{booking_id}/expire", status_code=200)
def expire_booking(booking_id: str, handler=Depends(get_expire_booking_handler)):
    command = ExpireBookingCommand(booking_id=BookingId(booking_id))

    try:
        handler.handle(command)
        return {"message": "Booking expired successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/checkin", status_code=200)
def checkin_booking(
    body: CheckinTicketSchema, handler=Depends(get_checkin_ticket_handler)
):
    command = CheckinTicketCommand(
        ticket_id=TicketId(body.ticket_code),
        ticket_code=TicketCode(body.ticket_code),
        event_id=EventId(body.event_id),
    )

    try:
        handler.handle(command)
        return {"message": "Ticket checked in successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{booking_id}/tickets", status_code=200)
def view_purchased_tickets(
    booking_id: str, handler=Depends(get_view_purchased_tickets_handler)
):
    query = ViewPurchasedTicketsQuery(booking_id=BookingId(booking_id))
    result = handler.handle(query)

    if result is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return result


@router.get("/{booking_id}/total-price", status_code=200)
def view_total_price(booking_id: str, handler=Depends(get_calculate_booking_handler)):
    query = CalculateBookingQuery(booking_id=BookingId(booking_id))
    result = handler.handle(query)

    if result is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return result
