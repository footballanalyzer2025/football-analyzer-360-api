from abc import ABC, abstractmethod
from typing import Any, Dict


class AnalysisStatsStrategy(ABC):

    @abstractmethod
    def execute(self,
                match_to_analyze: Dict[str, Any],
                all_teams: Dict[str, Dict[str, Any]],
                all_standings_competition: Dict):
        pass
