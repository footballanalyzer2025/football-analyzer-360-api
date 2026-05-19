from ...application.use_cases.stats.get_stats_use_case import GetStatsUseCase
from .web_container_federation import WebContainerFederation


class WebContainerStats:

    def __init__(self, web_container_federation: WebContainerFederation):
        self._web_container_federation = web_container_federation

    @property
    def get_stats_use_case(self) -> GetStatsUseCase:
        return GetStatsUseCase(
            self._web_container_federation.get_upcoming_matches_use_case
        )
    