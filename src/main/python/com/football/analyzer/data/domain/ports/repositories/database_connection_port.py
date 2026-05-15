from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class DatabaseConnectionPort(ABC):

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def get_collection(self, collection_name: str) -> Any:
        pass

    @abstractmethod
    def create_collection(self, collection_name: str, capped: bool = False, size: int = None, max_documents: int = None) -> bool:
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_collections(self) -> List[str]:
        pass

    @abstractmethod
    def drop_collection(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def rename_collection(self, old_name: str, new_name: str, drop_target: bool = False) -> bool:
        pass

    @abstractmethod
    def collection_stats(self, collection_name: str) -> Dict:
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, document: Dict) -> str:
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, documents: List[Dict]) -> List[str]:
        pass

    @abstractmethod
    def find(self, collection_name: str, query: Dict = None, projection: Dict = None) -> List[Dict]:
        pass

    @abstractmethod
    def find_one(self, collection_name: str, query: Dict = None, projection: Dict = None) -> Optional[Dict]:
        pass

    @abstractmethod
    def update_one(self, collection_name: str, query: Dict, update: Dict) -> int:
        pass

    @abstractmethod
    def delete_one(self, collection_name: str, query: Dict) -> int:
        pass

    @abstractmethod
    def delete_many(self, collection_name: str, query: Dict) -> int:
        pass
