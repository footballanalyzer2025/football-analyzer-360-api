from .web_container_federation import WebContainerFederation
from .web_container_standings import WebContainerStandings
from .web_container_team import WebContainerTeam
from ...application.use_cases.stats.get_stats_use_case import GetStatsUseCase


class WebContainerStats:

    def __init__(self,
                 web_container_federation: WebContainerFederation,
                 web_container_team: WebContainerTeam,
                 web_container_standings: WebContainerStandings):
        self._web_container_federation = web_container_federation
        self._web_container_team = web_container_team
        self._web_container_standings = web_container_standings

    @property
    def get_stats_use_case(self) -> GetStatsUseCase:
        return GetStatsUseCase(
            self._web_container_federation.get_upcoming_matches_use_case,
            self._web_container_team.get_all_teams_use_case,
            self._web_container_standings.get_standings_from_web_use_case
        )
    