from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class TeamRepositoryPort(ABC):

    @abstractmethod
    def get_collection(self):
        pass

    @abstractmethod
    def team_exists(self, team_name: str) -> bool:
        pass

    @abstractmethod
    def save_team(self, team_name: str, team_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def save_teams_batch(self, teams_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        pass

    @abstractmethod
    def get_all_team_names(self) -> List[str]:
        pass

    @abstractmethod
    def logical_delete_team(self, team_name: str) -> bool:
        pass

    @abstractmethod
    def find_by_name(self, team_name: str) -> Optional[Dict[str, Any]]:
        pass
