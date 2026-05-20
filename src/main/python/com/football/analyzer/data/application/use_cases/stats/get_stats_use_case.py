import logging
from dataclasses import dataclass
from typing import Dict, Any

from ..team.get_all_teams_use_case import GetAllTeamsUseCase
from ..team.get_teams_use_case import GetTeamsUseCase
from ...dto.federation_request_dto import GetCalendarsRequestDTO
from ...dto.stats_request_dto import StatsRequestDTO
from ..calendar.get_upcoming_matches_of_calendars_use_case import GetUpcomingMatchesUseCase
from ...dto.team_request_dto import GetTeamsRequestDTO

logger = logging.getLogger(__name__)


@dataclass
class GetStatsResult:
    success: bool
    message: str
    data: Dict[str, Any]


class GetStatsUseCase:

    def __init__(self,
                 get_upcoming_matches_use_case: GetUpcomingMatchesUseCase,
                 get_all_teams_use_case: GetAllTeamsUseCase):
        self._get_upcoming_matches_use_case = get_upcoming_matches_use_case
        self._get_all_teams_use_case = get_all_teams_use_case

    def execute(self, dto: StatsRequestDTO) -> GetStatsResult:
        validation_error = dto.validate()
        if validation_error:
            return GetStatsResult(
                success=False,
                message=validation_error,
                data={}
            )
        all_teams = self._get_all_teams_use_case.execute()
        upcoming_matches = self._get_upcoming_matches_use_case.execute(GetCalendarsRequestDTO(dto.stats_by_federation_and_competitions))
        return GetStatsResult(
            success=True,
            message="Stats endpoint ready (processing not yet implemented)",
            data={}
        )
    