from ..adapters.notifications.telegram_notification_adapter import TelegramNotificationAdapter
from ...application.services.notification_service import NotificationService
from ...domain.ports.notifications.notification_port import NotificationPort
from ...domain.value_objects.notification_config import NotificationConfig


class NotificationContainer:

    def __init__(self):
        self._telegram_adapter: NotificationPort = None
        self._notification_service: NotificationService = None

    @property
    def telegram_adapter(self) -> NotificationPort:
        if self._telegram_adapter is None:
            self._telegram_adapter = TelegramNotificationAdapter(NotificationConfig(enabled=True))
        return self._telegram_adapter

    @property
    def notification_service(self) -> NotificationService:
        if self._notification_service is None:
            channels = [self.telegram_adapter]
            self._notification_service = NotificationService(channels)
        return self._notification_service
