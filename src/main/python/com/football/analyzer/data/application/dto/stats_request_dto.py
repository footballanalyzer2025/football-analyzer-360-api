from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class StatsRequestDTO:
    stats_by_federation_and_competitions: Dict[str, List[str]]

    def validate(self) -> Optional[str]:
        if not self.stats_by_federation_and_competitions:
            return "stats_by_federation_and_competitions cannot be empty"
        return None
    