from abc import ABC, abstractmethod
from typing import Dict, List

from ..entities.team import Team


class TeamRepository(ABC):

    @abstractmethod
    def get_team_sessions(self, team: Team) -> Dict:
        pass

    @abstractmethod
    def get_team_matches(self, team: Team, season_filter: List[str]) -> Dict:
        pass
