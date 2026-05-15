from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class CreateOrUpdateFederationFromWebRequestDTO:
    competitions_by_federation: Dict[str, List[str]]

    def validate(self) -> Optional[str]:
        if not self.competitions_by_federation:
            return "competitions_by_federation cannot be empty"
        return None


@dataclass
class GetFederationsRequestDTO:
    competitions_by_federation: Dict[str, List[str]]

    def validate(self) -> Optional[str]:
        if not self.competitions_by_federation:
            return "competitions_by_federation cannot be empty"
        return None


@dataclass
class GetCalendarsRequestDTO:
    calendars_by_federation_and_competitions: Dict[str, List[str]]

    def validate(self) -> Optional[str]:
        if not self.calendars_by_federation_and_competitions:
            return "calendars_by_federation_and_competitions cannot be empty"
        return None


@dataclass
class DeleteFederationRequestDTO:
    federation_name: str

    def validate(self) -> Optional[str]:
        if not self.federation_name:
            return "federation_name cannot be empty"
        return None
