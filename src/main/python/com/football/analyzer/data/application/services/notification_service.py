import logging
from typing import Dict, Any, List

from ...domain.ports.notifications.notification_port import NotificationPort

logger = logging.getLogger(__name__)


class NotificationService:

    def __init__(self, channels: List[NotificationPort]):
        self._channels = channels

    def send_message(self, message: str, **kwargs) -> Dict[str, bool]:
        results = {}
        for channel in self._channels:
            try:
                results[channel.__class__.__name__] = channel.send_message(message, **kwargs)
            except Exception as e:
                logging.error(f'Notification Service Error {e.__cause__}')
                results[channel.__class__.__name__] = False
        return results

    def send_success(self, title: str, details: Dict[str, Any]) -> Dict[str, bool]:
        results = {}
        for channel in self._channels:
            try:
                results[channel.__class__.__name__] = channel.send_success(title, details)
            except Exception as e:
                logging.error(f'Notification Service Error {e.__cause__}')
                results[channel.__class__.__name__] = False
        return results

    def send_error(self, title: str, error: Exception, context: Dict[str, Any]) -> Dict[str, bool]:
        results = {}
        for channel in self._channels:
            try:
                results[channel.__class__.__name__] = channel.send_error(title, error, context)
            except Exception as e:
                logging.error(f'Notification Service Error {e.__cause__}')
                results[channel.__class__.__name__] = False
        return results
