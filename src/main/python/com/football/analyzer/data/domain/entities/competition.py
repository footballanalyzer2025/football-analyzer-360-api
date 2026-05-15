from dataclasses import dataclass
from typing import Optional

from .federation import Federation


@dataclass
class Competition:
    name: str
    url: str
    federation: Optional[Federation] = None
    season: Optional[str] = None

    def __hash__(self):
        return hash(self.url)
