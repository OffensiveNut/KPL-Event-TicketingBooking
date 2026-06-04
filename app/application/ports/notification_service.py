from abc import ABC, abstractmethod

from app.domain.value_objects.user_id import UserId


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user_id: UserId, message: str) -> None:
        """Send an email or WhatsApp notification to a user."""
