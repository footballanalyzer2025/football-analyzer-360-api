from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class CreateOrUpdateManagerDateRequestDTO:
    managers_data: Dict[str, str]

    def validate(self) -> Optional[str]:
        if not self.managers_data:
            return "managers_data cannot be empty"
        return None


@dataclass
class GetManagersDateRequestDTO:
    team_managers: List[str]

    def validate(self) -> Optional[str]:
        if not self.team_managers:
            return "team_managers cannot be empty"
        return None


@dataclass
class DeleteManagerDateRequestDTO:
    team_name: str

    def validate(self) -> Optional[str]:
        if not self.team_name:
            return "team_name cannot be empty"
        return None
