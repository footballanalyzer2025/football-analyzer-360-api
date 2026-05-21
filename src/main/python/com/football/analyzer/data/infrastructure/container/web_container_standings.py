from ...application.use_cases.standings.get_standings_from_web_use_case import GetStandingsFromWebUseCase


class WebContainerStandings:

    def __init__(self, federation_repository):
        self._federation_repository = federation_repository

    @property
    def get_standings_use_case(self) -> GetStandingsFromWebUseCase:
        return GetStandingsFromWebUseCase(self._federation_repository)
