from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.models.event_model import Base, EventModel, TicketCategoryModel


class BookingModel(Base):
    __tablename__ = "bookings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    event_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    customer_id: Mapped[str] = mapped_column(String(36), nullable=False)
    ticket_category_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("ticket_categories.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    payment_deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ticket_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    service_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    tickets: Mapped[list["TicketModel"]] = relationship(
        "TicketModel",
        back_populates="booking",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    refunds: Mapped[list["RefundModel"]] = relationship(
        "RefundModel",
        back_populates="booking",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    event: Mapped[EventModel] = relationship("EventModel")
    ticket_category: Mapped[TicketCategoryModel] = relationship("TicketCategoryModel")
