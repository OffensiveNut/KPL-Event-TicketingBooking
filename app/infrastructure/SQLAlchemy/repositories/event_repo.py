from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.domain.aggregates.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.domain.repositories.event_repository import EventRepository
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.event_status import EventStatus
from app.domain.value_objects.ticket_category_id import TicketCategoryId
from app.domain.value_objects.user_id import UserId
from app.infrastructure.models.event_model import EventModel, TicketCategoryModel


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, event: Event) -> None:
        model = self._to_model(event)
        self._session.merge(model)

    def get_by_id(self, event_id: EventId) -> Event | None:
        model = self._session.get(EventModel, event_id.value)
        if model is None:
            return None
        return self._to_domain(model)

    def list_published(
        self,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
        location: str | None = None,
    ) -> list[Event]:
        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.ticket_categories))
            .where(EventModel.status == EventStatus.PUBLISHED.value)
        )

        if start_date is not None:
            stmt = stmt.where(EventModel.start_date >= start_date)
        if end_date is not None:
            stmt = stmt.where(EventModel.end_date <= end_date)
        if location is not None:
            stmt = stmt.where(EventModel.location == location)

        models = self._session.scalars(stmt).all()
        return [self._to_domain(model) for model in models]

    def _to_model(self, event: Event) -> EventModel:
        ticket_categories = [
            TicketCategoryModel(
                id=category.id.value,
                event_id=event.id.value,
                name=category.name,
                price=category.price.amount,
                quota=category.quota,
                sales_start_date=category.sales_period.start_date,
                sales_end_date=category.sales_period.end_date,
                is_active=category.is_active,
            )
            for category in event._ticket_categories
        ]

        return EventModel(
            id=event.id.value,
            organizer_id=event.event_organizer.value,
            name=event.name,
            description=event.description,
            start_date=event.date.start_date,
            end_date=event.date.end_date,
            location=event.location,
            max_capacity=event.max_capacity,
            status=event.status.value,
            ticket_categories=ticket_categories,
        )

    def _to_domain(self, model: EventModel) -> Event:
        event = Event(
            event_name=model.name,
            description=model.description,
            start_date=model.start_date,
            end_date=model.end_date,
            location=model.location,
            max_capacity=model.max_capacity,
            event_organizer=UserId(model.organizer_id),
        )

        event.id = EventId(model.id)
        event.status = EventStatus(model.status)
        event._domain_events = []
        event._ticket_categories = [
            self._to_domain_ticket_category(category)
            for category in model.ticket_categories
        ]
        return event

    def _to_domain_ticket_category(self, model: TicketCategoryModel) -> TicketCategory:
        category = TicketCategory(
            name=model.name,
            price=model.price,
            quota=model.quota,
            sales_start_date=model.sales_start_date,
            sales_end_date=model.sales_end_date,
        )
        category.id = TicketCategoryId(model.id)
        category.is_active = model.is_active
        return category
