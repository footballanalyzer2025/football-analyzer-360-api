from abc import ABC, abstractmethod
from typing import Dict, Any, List


class FederationRepositoryPort(ABC):

    @abstractmethod
    def get_collection(self):
        pass

    @abstractmethod
    def federation_exists(self, federation_name: str) -> bool:
        pass

    @abstractmethod
    def save_federation(self, federation_name: str, federation_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def save_federations_batch(self, federations_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        pass

    @abstractmethod
    def get_all_federation_names(self) -> List[str]:
        pass
