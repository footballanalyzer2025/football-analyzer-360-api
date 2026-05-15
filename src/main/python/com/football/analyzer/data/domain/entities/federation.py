from dataclasses import dataclass
from typing import List


@dataclass
class Federation:
    name: str
    url: str
    competitions: List[str] = None

    def __post_init__(self):
        if self.competitions is None:
            self.competitions = []
