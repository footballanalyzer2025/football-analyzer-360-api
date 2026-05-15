from abc import ABC, abstractmethod
from typing import Dict, Any


class NotificationPort(ABC):

    @abstractmethod
    def send_message(self, message: str, **kwargs) -> bool:
        pass

    @abstractmethod
    def send_success(self, title: str, details: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def send_error(self, title: str, error: Exception, context: Dict[str, Any]) -> bool:
        pass
