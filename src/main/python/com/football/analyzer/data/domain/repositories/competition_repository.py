from abc import ABC, abstractmethod
from typing import List, Dict

from ..entities.competition import Competition


class CompetitionRepository(ABC):

    @abstractmethod
    def get_active_competitions(self) -> Dict[str, List[str]]:
        pass

    @abstractmethod
    def get_competition_sections(self, competition: Competition) -> Dict:
        pass

    @abstractmethod
    def get_teams(self, competition: Competition) -> List[Dict]:
        pass
