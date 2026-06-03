from sqlalchemy.orm import Session

from app.infrastructure.repositories.booking_repo import SqlAlchemyBookingRepository
from app.infrastructure.repositories.event_repo import SqlAlchemyEventRepository
from app.infrastructure.repositories.refund_repo import SqlAlchemyRefundRepository
from app.usecases.interfaces.unit_of_work import UnitOfWork


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
