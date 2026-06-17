from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from app.api.v1.schemas.refund_schema import (
    MarkRefundAsPaidOutSchema,
    RejectRefundSchema,
    RequestRefundSchema,
)
from app.application.usecases.refund.commands import (
    ApproveRefundCommand,
    MarkRefundAsPaidOutCommand,
    RejectRefundCommand,
    RequestRefundCommand,
)
from app.core.dependencies import (
    get_approve_refund_handler,
    get_mark_refund_paid_out_handler,
    get_reject_refund_handler,
    get_request_refund_handler,
)
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.refund_id import RefundId

router = APIRouter(prefix="/refunds", tags=["refunds"])


@router.post("/request", status_code=201)
def request_refund(
    body: RequestRefundSchema, handler=Depends(get_request_refund_handler)
):
    command = RequestRefundCommand(
        booking_id=BookingId(body.booking_id),
        event_id=EventId(body.event_id),
    )
    try:
        handler.handle(command)
        return {"message": "Refund requested successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{refund_id}/approve", status_code=200)
def approve_refund(refund_id: str, handler=Depends(get_approve_refund_handler)):
    command = ApproveRefundCommand(refund_id=RefundId(refund_id))
    try:
        handler.handle(command)
        return {"message": "Refund approved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{refund_id}/reject", status_code=200)
def reject_refund(
    refund_id: str,
    body: RejectRefundSchema,
    handler=Depends(get_reject_refund_handler),
):
    command = RejectRefundCommand(
        refund_id=RefundId(refund_id),
        rejection_reason=body.rejection_reason,
    )
    try:
        handler.handle(command)
        return {"message": "Refund rejected successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{refund_id}/pay-out", status_code=200)
def mark_refund_paid_out(
    refund_id: str,
    body: MarkRefundAsPaidOutSchema,
    handler=Depends(get_mark_refund_paid_out_handler),
):
    command = MarkRefundAsPaidOutCommand(
        refund_id=RefundId(refund_id),
        payment_reference=body.payment_reference,
    )
    try:
        handler.handle(command)
        return {"message": "Refund paid out successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
