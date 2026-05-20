import logging
from dataclasses import dataclass
from typing import Dict, Any

from main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from ..team.get_all_teams_use_case import GetAllTeamsUseCase
from ...dto.federation_request_dto import GetCalendarsRequestDTO
from ...dto.stats_request_dto import StatsRequestDTO
from ..calendar.get_upcoming_matches_of_calendars_use_case import GetUpcomingMatchesUseCase

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
        self._config_loader = ConfigLoader()

    def execute(self, dto: StatsRequestDTO) -> GetStatsResult:
        validation_error = dto.validate()
        if validation_error:
            return GetStatsResult(
                success=False,
                message=validation_error,
                data={}
            )
        all_teams = self._get_all_teams_data()
        upcoming_matches_by_federation_and_competition = self._get_upcoming_matches_use_case.execute(
            GetCalendarsRequestDTO(dto.stats_by_federation_and_competitions)
        ).upcoming_matches_by_federation_and_competition
        for federation, competitions in list(upcoming_matches_by_federation_and_competition.items()):
            for competition_name, competition_data in list(competitions.items()):
                standings_url = self._get_standings_url(competition_data, federation)
                if competition_data[ConfigConstants.TOTAL_UPCOMING] > 0:
                    upcoming_matches = competition_data[ConfigConstants.UPCOMING_MATCHES]
                    are_there_any_matches_to_analyze = False
                    for match in upcoming_matches:
                        home_team_name = match[ConfigConstants.HOME_TEAM]
                        away_team_name = match[ConfigConstants.AWAY_TEAM]
                        if home_team_name in all_teams and away_team_name in all_teams and ConfigConstants.MATCHES in all_teams[home_team_name] and ConfigConstants.MATCHES in all_teams[away_team_name]:
                            home_team_matches = all_teams[home_team_name][ConfigConstants.MATCHES][ConfigConstants.ALL_MATCHES]
                            away_team_matches = all_teams[away_team_name][ConfigConstants.MATCHES][ConfigConstants.ALL_MATCHES]
                            match['status'] = self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_TO_ANALYZE)
                            match['stats'] = {}
                            are_there_any_matches_to_analyze = True
                    if not are_there_any_matches_to_analyze:
                        self._delete_items_without_matches_to_analyze(competition_name, competitions, federation, upcoming_matches_by_federation_and_competition)
                else:
                    self._delete_items_without_matches_to_analyze(competition_name, competitions, federation, upcoming_matches_by_federation_and_competition)
        return GetStatsResult(
            success=True,
            message="Stats endpoint ready (processing not yet implemented)",
            data=upcoming_matches_by_federation_and_competition
        )

    def _get_all_teams_data(self):
        all_teams_data = self._get_all_teams_use_case.execute().teams
        return {item[ConfigConstants.NAME]: item for item in all_teams_data}

    def _get_standings_url(self, competition_data, federation):
        standings_url = competition_data[self._config_loader.get_results_and_standings_section()][ConfigConstants.MAIN_URL]
        if federation == ConfigConstants.FIFA:
            standings_url = self._config_loader.get_fifa_world_ranking_url_special_case()
        return standings_url

    @staticmethod
    def _delete_items_without_matches_to_analyze(competition_name, competitions, federation, upcoming_matches_by_federation_and_competition):
        del competitions[competition_name]
        if upcoming_matches_by_federation_and_competition[federation] == {}:
            del upcoming_matches_by_federation_and_competition[federation]
    