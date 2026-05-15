from abc import ABC, abstractmethod
from typing import Dict, Any


class DataSourcePort(ABC):

    @abstractmethod
    def get_main_data(self, competitions_by_federation: Dict) -> Dict[str, Any]:
        pass
