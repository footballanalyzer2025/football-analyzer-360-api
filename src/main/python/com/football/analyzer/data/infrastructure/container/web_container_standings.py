from .web_container_federation import WebContainerFederation
from ...application.use_cases.standings.get_standings_from_web_use_case import GetStandingsFromWebUseCase


class WebContainerStandings:

    def __init__(self, web_container_federation: WebContainerFederation):
        self._web_container_federation = web_container_federation

    @property
    def get_standings_from_web_use_case(self) -> GetStandingsFromWebUseCase:
        return GetStandingsFromWebUseCase(self._web_container_federation.federation_repository)
