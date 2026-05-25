import logging
from dataclasses import dataclass
from typing import Dict, Any, List

from main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from main.python.com.football.analyzer.data.infrastructure.helpers.competition_type_helper import CompetitionTypeHelper
from ..calendar.get_upcoming_matches_of_calendars_use_case import GetUpcomingMatchesUseCase
from ..standings.get_standings_from_web_use_case import GetStandingsFromWebUseCase
from ..team.get_all_teams_use_case import GetAllTeamsUseCase
from ...dto.federation_request_dto import GetCalendarsRequestDTO
from ...dto.standings_request_dto import StandingsRequestDTO
from ...dto.stats_request_dto import StatsRequestDTO

logger = logging.getLogger(__name__)


@dataclass
class GetStatsResult:
    success: bool
    message: str
    data: Dict[str, Any]


class GetStatsUseCase:

    def __init__(self,
                 get_upcoming_matches_use_case: GetUpcomingMatchesUseCase,
                 get_all_teams_use_case: GetAllTeamsUseCase,
                 get_standings_from_web_use_case: GetStandingsFromWebUseCase):
        self._get_upcoming_matches_use_case = get_upcoming_matches_use_case
        self._get_all_teams_use_case = get_all_teams_use_case
        self._get_standings_from_web_use_case = get_standings_from_web_use_case
        self._config_loader = ConfigLoader()
        self._competition_type_helper = CompetitionTypeHelper()

    def execute(self, dto: StatsRequestDTO) -> GetStatsResult:
        validation_error = dto.validate()
        if validation_error:
            return GetStatsResult(
                success=False,
                message=validation_error,
                data={}
            )
        all_teams = self._get_all_teams_indexed_by_name()
        upcoming_matches = self._get_upcoming_matches(dto)
        standings = self._get_standings(dto)
        self._process_upcoming_matches(upcoming_matches, all_teams, standings)
        return GetStatsResult(
            success=True,
            message="Stats processed successfully",
            data=upcoming_matches
        )

    def _get_all_teams_indexed_by_name(self) -> Dict[str, Dict[str, Any]]:
        all_teams_data = self._get_all_teams_use_case.execute().teams
        return {item[ConfigConstants.NAME]: item for item in all_teams_data}

    def _get_upcoming_matches(self, dto: StatsRequestDTO) -> Dict[str, Any]:
        return self._get_upcoming_matches_use_case.execute(
            GetCalendarsRequestDTO(dto.stats_by_federation_and_competitions)
        ).upcoming_matches_by_federation_and_competition

    def _get_standings(self, dto: StatsRequestDTO) -> Dict[str, Any]:
        return self._get_standings_from_web_use_case.execute(
            StandingsRequestDTO(dto.stats_by_federation_and_competitions)
        ).standings_data

    def _process_upcoming_matches(self,
                                  upcoming_matches: Dict[str, Any],
                                  all_teams: Dict[str, Dict[str, Any]],
                                  standings: Dict[str, Any]) -> None:
        federations_to_remove = []
        for federation, competitions in upcoming_matches.items():
            competitions_to_remove = self._process_competitions(federation, competitions, all_teams, standings)
            self._remove_empty_competitions(competitions, competitions_to_remove)
            if not competitions:
                federations_to_remove.append(federation)
        self._remove_empty_federations(upcoming_matches, federations_to_remove)

    def _process_competitions(self,
                              federation: str,
                              competitions: Dict[str, Any],
                              all_teams: Dict[str, Dict[str, Any]],
                              standings: Dict[str, Any]) -> List[str]:
        competitions_to_remove = []
        if federation in standings:
            for competition_name, competition_data in competitions.items():
                if competition_name in standings[federation]:
                    if ConfigConstants.STANDINGS_DATA in standings[federation][competition_name]:
                        competition_type = self._competition_type_helper.get_competition_type(federation, competition_name)
                        has_matches_to_analyze = self._process_competition_matches(competition_type, competition_data, all_teams, standings[federation][competition_name][ConfigConstants.STANDINGS_DATA])
                        if not has_matches_to_analyze:
                            competitions_to_remove.append(competition_name)
        return competitions_to_remove

    @staticmethod
    def _remove_empty_competitions(competitions: Dict[str, Any], competitions_to_remove: List[str]) -> None:
        for comp_name in competitions_to_remove:
            del competitions[comp_name]

    @staticmethod
    def _remove_empty_federations(upcoming_matches: Dict[str, Any], federations_to_remove: List[str]) -> None:
        for federation in federations_to_remove:
            del upcoming_matches[federation]

    def _process_competition_matches(self,
                                     competition_type: str,
                                     competition_data: Dict[str, Any],
                                     all_teams: Dict[str, Dict[str, Any]],
                                     standings: Dict[str, Any]) -> bool:
        has_matches_to_analyze = False
        if self._is_total_upcoming_more_than_zero(competition_data):
            upcoming_matches = competition_data.get(ConfigConstants.UPCOMING_MATCHES, [])
            has_matches_to_analyze = self._get_matches_to_analyze(all_teams, has_matches_to_analyze, upcoming_matches)
            if has_matches_to_analyze:
                self._get_stats_of_upcoming_matches(competition_type, all_teams, upcoming_matches, standings)
        return has_matches_to_analyze

    @staticmethod
    def _is_total_upcoming_more_than_zero(competition_data):
        has_matches_to_analyze = False
        total_upcoming = competition_data.get(ConfigConstants.TOTAL_UPCOMING, 0)
        if total_upcoming > 0:
            has_matches_to_analyze = True
        return has_matches_to_analyze

    def _get_matches_to_analyze(self, all_teams, has_matches_to_analyze, upcoming_matches):
        for match in upcoming_matches:
            if self._is_match_ready_for_analysis(match, all_teams):
                self._mark_match_for_analysis(match)
                has_matches_to_analyze = True
        return has_matches_to_analyze

    @staticmethod
    def _is_match_ready_for_analysis(match: Dict[str, Any], all_teams: Dict[str, Dict[str, Any]]) -> bool:
        home_team = match.get(ConfigConstants.HOME_TEAM)
        away_team = match.get(ConfigConstants.AWAY_TEAM)
        if not home_team or not away_team:
            return False
        home_team_data = all_teams.get(home_team)
        away_team_data = all_teams.get(away_team)
        if not home_team_data or not away_team_data:
            return False
        return ConfigConstants.MATCHES in home_team_data and ConfigConstants.MATCHES in away_team_data

    def _mark_match_for_analysis(self, match: Dict[str, Any]) -> None:
        match[ConfigConstants.STATUS] = self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_TO_ANALYZE)
        match[ConfigConstants.STATS] = {}

    def _get_stats_of_upcoming_matches(self, competition_type: str, all_teams, upcoming_matches, standings):
        for match in upcoming_matches:
            if self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_TO_ANALYZE) == match[ConfigConstants.STATUS]:
                self._get_stats_to_match(competition_type, match, all_teams, standings)

    @staticmethod
    def _get_stats_to_match(competition_type: str, match: Dict[str, Any], all_teams: Dict[str, Dict[str, Any]], standing_competition: Any) -> None:
        # TODO get stats of the match
        home_team_matches = all_teams[match[ConfigConstants.HOME_TEAM]][ConfigConstants.MATCHES][ConfigConstants.ALL_MATCHES]
        away_team_matches = all_teams[match[ConfigConstants.AWAY_TEAM]][ConfigConstants.MATCHES][ConfigConstants.ALL_MATCHES]
