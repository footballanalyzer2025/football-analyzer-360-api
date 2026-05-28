from abc import ABC, abstractmethod
from typing import Dict, List


class MatchStandingsStatsPort(ABC):

    @abstractmethod
    def get_match_standings_stats(self, standing: Dict, team_matches: List, opponent: str) -> Dict:
        pass
