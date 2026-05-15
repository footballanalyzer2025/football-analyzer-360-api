from typing import Dict

from src.main.python.com.football.analyzer.data.domain.entities.team import Team
from src.main.python.com.football.analyzer.data.domain.repositories.team_repository import TeamRepository
from src.main.python.com.football.analyzer.data.domain.services.season_filter_service import SeasonFilterService


class GetTeamMatchesUseCase:

    def __init__(self, team_repository: TeamRepository, season_filter_service: SeasonFilterService):
        self.team_repository = team_repository
        self.season_filter_service = season_filter_service

    def execute(self, team: Team, manager_start_date: str) -> Dict:
        first_session = self._get_first_session(team)
        season_filter = self.season_filter_service.get_season_filter(first_session, manager_start_date)
        return self.team_repository.get_team_matches(team, season_filter)

    def _get_first_session(self, team: Team) -> str:
        sessions = self.team_repository.get_team_sessions(team)
        return next(iter(sessions)) if sessions else ""
