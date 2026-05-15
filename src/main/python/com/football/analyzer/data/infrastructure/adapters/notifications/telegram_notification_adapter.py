import logging
import requests
from typing import Dict, Any

from ....domain.ports.notifications.notification_port import NotificationPort
from ....domain.value_objects.notification_config import NotificationConfig
from ....commons.config.config_loader import ConfigLoader
from ....commons.config.config_constants import ConfigConstants

logger = logging.getLogger(__name__)


class TelegramNotificationAdapter(NotificationPort):

    def __init__(self, config: NotificationConfig = None):
        self.config = config or NotificationConfig()
        self._load_telegram_config()
        self._base_url = f"https://api.telegram.org/bot{self._token}/sendMessage"

    def _load_telegram_config(self):
        config_loader = ConfigLoader()
        telegram_config = config_loader.get_telegram_config()
        self._token = telegram_config.get(ConfigConstants.TOKEN)
        self._chat_id = telegram_config.get(ConfigConstants.CHAT_ID)

        if not self._token or not self._chat_id:
            logger.warning("Telegram configuration incomplete. Notifications will be disabled.")
            self.config.enabled = False

    def _send(self, text: str) -> bool:
        if not self.config.enabled:
            logger.debug("Telegram notifications are disabled")
            return False

        try:
            payload = {
                'chat_id': self._chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            response = requests.post(self._base_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Telegram notification sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False

    def send_message(self, message: str, **kwargs) -> bool:
        return self._send(message)

    def send_success(self, title: str, details: Dict[str, Any]) -> bool:
        message = self._format_success_message(title, details)
        return self._send(message)

    def send_error(self, title: str, error: Exception, context: Dict[str, Any]) -> bool:
        message = self._format_error_message(title, error, context)
        return self._send(message)

    @staticmethod
    def _format_success_message(title: str, details: Dict[str, Any]) -> str:
        lines = [f"✅ <b>{title}</b>", ""]
        for key, value in details.items():
            lines.append(f"▫️ {key}: {value}")
        return "\n".join(lines)

    @staticmethod
    def _format_error_message(title: str, error: Exception, context: Dict[str, Any]) -> str:
        lines = [f"❌ <b>{title}</b>", f"Error: {str(error)}", ""]
        if context:
            lines.append("\nContexto:")
            for key, value in context.items():
                lines.append(f"▫️ {key}: {value}")
        return "\n".join(lines)
