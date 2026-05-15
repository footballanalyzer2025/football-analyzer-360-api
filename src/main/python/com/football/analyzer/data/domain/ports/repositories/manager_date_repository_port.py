from abc import ABC, abstractmethod
from typing import Dict, Optional


class ManagerDateRepositoryPort(ABC):

    @abstractmethod
    def get_collection(self):
        pass

    @abstractmethod
    def save(self, team_name: str, start_date: str) -> bool:
        pass

    @abstractmethod
    def save_many(self, managers_data: Dict[str, str]) -> Dict[str, bool]:
        pass

    @abstractmethod
    def get(self, team_name: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_all(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def delete(self, team_name: str) -> bool:
        pass

    @abstractmethod
    def delete_all(self) -> int:
        pass

    @abstractmethod
    def exists(self, team_name: str) -> bool:
        pass
