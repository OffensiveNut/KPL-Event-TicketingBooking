from sqlalchemy.orm import Session

from app.application.ports.unit_of_work import UnitOfWork
from app.infrastructure.SQLAlchemy.repositories.booking_repo import SqlAlchemyBookingRepository
from app.infrastructure.SQLAlchemy.repositories.event_repo import SqlAlchemyEventRepository
from app.infrastructure.SQLAlchemy.repositories.refund_repo import SqlAlchemyRefundRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: Session):
        self._session = session
        self.events = SqlAlchemyEventRepository(session)
        self.bookings = SqlAlchemyBookingRepository(session)
        self.refunds = SqlAlchemyRefundRepository(session)

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
