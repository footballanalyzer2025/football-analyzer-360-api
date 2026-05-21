from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class StandingsRequestDTO:
    standings_by_federation_and_competitions: Dict[str, List[str]]

    def validate(self) -> Optional[str]:
        if not self.standings_by_federation_and_competitions:
            return "standings_by_federation_and_competitions cannot be empty"
        return None
    