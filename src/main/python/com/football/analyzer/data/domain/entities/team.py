from dataclasses import dataclass
from typing import Optional


@dataclass
class Team:
    name: str
    url: str
    manager_start_date: Optional[str] = None
    competitions: list = None

    def __hash__(self):
        return hash(self.url)
    