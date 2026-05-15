import logging
from dataclasses import dataclass
from typing import Dict, Any

from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from src.main.python.com.football.analyzer.data.application.dto.federation_request_dto import GetCalendarsRequestDTO
from .get_calendars_use_case import GetCalendarsUseCase

NUMBER_OF_TEAMS_DEFAULT = 0
MIN_LIMIT = 1
GAMES_BY_TOTAL_TEAMS = 2
PROJECTION_GAMES = 3

logger = logging.getLogger(__name__)


@dataclass
class GetUpcomingMatchesResult:
    success: bool
    message: str
    upcoming_matches_by_federation_and_competition: Dict[str, Dict[str, Any]]


class GetUpcomingMatchesUseCase:

    def __init__(self, get_calendars_use_case: GetCalendarsUseCase):
        self._get_calendars_use_case = get_calendars_use_case
        self._config_loader = ConfigLoader()
        self._calendar_section = self._config_loader.get_calendar_section()
        self._upcoming_status = self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_UPCOMING_SELECTOR)

    def execute(self, dto: GetCalendarsRequestDTO) -> GetUpcomingMatchesResult:
        calendars_result = self._get_calendars_use_case.execute(dto)
        if not calendars_result.success:
            return GetUpcomingMatchesResult(
                success=False,
                message=calendars_result.message,
                upcoming_matches_by_federation_and_competition={}
            )
        result = self._get_upcoming_matches_by_federations(calendars_result)
        return GetUpcomingMatchesResult(
            success=True,
            message=f"Retrieved upcoming matches for {len(result)} federations",
            upcoming_matches_by_federation_and_competition=result
        )

    def _get_upcoming_matches_by_federations(self, calendars_result):
        result = {}
        for fed_name, competitions in calendars_result.calendars_by_federation_and_competitions.items():
            fed_result = self._get_upcoming_matches_by_competitions(competitions)
            if fed_result:
                result[fed_name] = fed_result
        return result

    def _get_upcoming_matches_by_competitions(self, competitions):
        fed_result = {}
        for comp_name, comp_data in competitions.items():
            all_matches = comp_data.get(self._calendar_section, {}).get(ConfigConstants.MATCHES, []).get(ConfigConstants.ALL_MATCHES, [])
            upcoming_matches = [m for m in all_matches if m.get(ConfigConstants.STATUS) == self._upcoming_status]
            number_of_teams = comp_data.get(ConfigConstants.NUMBER_OF_TEAMS, NUMBER_OF_TEAMS_DEFAULT)
            limit = max(MIN_LIMIT, (number_of_teams // GAMES_BY_TOTAL_TEAMS) * PROJECTION_GAMES) if number_of_teams > NUMBER_OF_TEAMS_DEFAULT else NUMBER_OF_TEAMS_DEFAULT
            limited_matches = upcoming_matches[:limit]
            fed_result[comp_name] = {
                ConfigConstants.UPCOMING_MATCHES: limited_matches,
                ConfigConstants.TOTAL_UPCOMING: len(limited_matches),
                ConfigConstants.LIMIT_APPLIED: limit,
                ConfigConstants.NUMBER_OF_TEAMS: number_of_teams
            }
        return fed_result
