from pydantic import BaseModel


class RequestRefundSchema(BaseModel):
    booking_id: str
    event_id: str


class RejectRefundSchema(BaseModel):
    rejection_reason: str


class MarkRefundAsPaidOutSchema(BaseModel):
    payment_reference: str
