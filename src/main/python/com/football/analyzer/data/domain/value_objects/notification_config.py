from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationConfig:
    enabled: bool = True
