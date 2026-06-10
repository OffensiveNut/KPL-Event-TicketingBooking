from decimal import Decimal

from pydantic import BaseModel


class CreateBookingSchema(BaseModel):
    event_id: str
    ticket_category_id: str
    ticket_category_name: str
    ticket_quantity: int
    price: Decimal
    service_fee: Decimal


class PayBookingSchema(BaseModel):
    payment_amount: Decimal


class CheckinTicketSchema(BaseModel):
    ticket_id: str
    ticket_code: str
    event_id: str
