from typing import Dict, Any

from src.main.python.com.football.analyzer.data.application.services.web_scrapping_competitions_by_federations_orchestrator_service import WebScrappingCompetitionsByFederationsOrchestratorService
from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.domain.ports.services.data_source_port import DataSourcePort
from src.main.python.com.football.analyzer.data.infrastructure.container.web_scrapping_data_source_container import WebScrappingDataSourceContainer


class WebScrappingCompetitionsByFederationsDataSourceAdapter(DataSourcePort):

    def __init__(
            self,
            timeout: int = 5,
            headers: dict = None
    ):
        if headers is None:
            headers = ConfigConstants.HEADERS
        self.web_scrapping_competitions_by_federations_orchestrator_service = WebScrappingCompetitionsByFederationsOrchestratorService(
            WebScrappingDataSourceContainer(
                timeout=timeout,
                headers=headers
            )
        )

    def get_main_data(self, competitions_by_federation: Dict) -> Dict[str, Any]:
        return self.web_scrapping_competitions_by_federations_orchestrator_service.execute(competitions_by_federation)
