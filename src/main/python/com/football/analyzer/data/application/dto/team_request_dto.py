from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class CreateTeamsFromWebRequestDTO:
    competitions_by_federation: Dict[str, Dict[str, Union[str, List[str]]]]

    def validate(self) -> Optional[str]:
        if not self.competitions_by_federation:
            return "competitions_by_federation cannot be empty"
        return None


@dataclass
class CreateTeamsFromListRequestDTO:
    teams_to_create: List[str]

    def validate(self) -> Optional[str]:
        if not self.teams_to_create:
            return "teams_to_create cannot be empty"
        return None


@dataclass
class GetTeamsRequestDTO:
    teams_data: List[str]

    def validate(self) -> Optional[str]:
        if not self.teams_data:
            return "teams_data cannot be empty"
        return None


@dataclass
class DeleteTeamRequestDTO:
    team_to_delete: str

    def validate(self) -> Optional[str]:
        if not self.team_to_delete:
            return "team_name cannot be empty"
        return None
