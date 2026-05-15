from typing import Dict, Any

from src.main.python.com.football.analyzer.data.application.services.web_scrapping_team_matches_orchestrator_service import WebScrappingTeamMatchesOrchestratorService
from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.domain.ports.services.data_source_port import DataSourcePort
from src.main.python.com.football.analyzer.data.infrastructure.container.web_scrapping_data_source_container import WebScrappingDataSourceContainer


class WebScrappingTeamMatchesDataSourceAdapter(DataSourcePort):

    def __init__(
            self,
            timeout: int = 5,
            headers: dict = None,
            managers_data: dict = None
    ):
        if headers is None:
            headers = ConfigConstants.HEADERS
        self.web_scrapping_team_matches_orchestrator_service = WebScrappingTeamMatchesOrchestratorService(
            WebScrappingDataSourceContainer(
                timeout=timeout,
                headers=headers
            ),
            managers_data
        )

    def get_main_data(self, teams_data: Dict) -> Dict[str, Any]:
        return self.web_scrapping_team_matches_orchestrator_service.execute(teams_data)
