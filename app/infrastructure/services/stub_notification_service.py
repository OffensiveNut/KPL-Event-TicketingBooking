import logging

from app.domain.value_objects.user_id import UserId
from app.usecases.interfaces.notification_service import NotificationService

logger = logging.getLogger(__name__)


class StubNotificationService(NotificationService):
    def send_notification(self, user_id: UserId, message: str) -> None:
        # dummy implementation
        logger.info(f"[StubNotificationService] To User {user_id.value}: {message}")
