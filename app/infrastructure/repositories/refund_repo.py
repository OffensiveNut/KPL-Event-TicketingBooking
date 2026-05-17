from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.aggregates.refund import Refund
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.value_objects.booking_id import BookingId
from app.domain.value_objects.money import Money
from app.domain.value_objects.refund_id import RefundId
from app.domain.value_objects.refund_status import RefundStatus
from app.infrastructure.models.booking_model import RefundModel


class SqlAlchemyRefundRepository(RefundRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, refund: Refund) -> None:
        model = RefundModel(
            id=refund.id.value,
            booking_id=refund.booking_id.value,
            amount=refund.amount.amount,
            status=refund.status.value,
            rejection_reason=refund.rejection_reason,
            payment_reference=refund.payment_reference,
        )
        self._session.merge(model)

    def get_by_id(self, refund_id: RefundId) -> Refund | None:
        model = self._session.get(RefundModel, refund_id.value)
        if model is None:
            return None
        return self._to_domain(model)

    def get_by_booking_id(self, booking_id: BookingId) -> Refund | None:
        stmt = select(RefundModel).where(RefundModel.booking_id == booking_id.value)
        model = self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_domain(model)

    def _to_domain(self, model: RefundModel) -> Refund:
        refund = Refund(
            booking_id=BookingId(model.booking_id),
            amount=Money(model.amount),
        )
        refund.id = RefundId(model.id)
        refund.status = RefundStatus(model.status)
        refund.rejection_reason = model.rejection_reason
        refund.payment_reference = model.payment_reference
        refund._domain_events = []
        return refund
