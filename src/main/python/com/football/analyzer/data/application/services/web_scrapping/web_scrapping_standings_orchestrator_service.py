import logging
from typing import Dict

from main.python.com.football.analyzer.data.infrastructure.container.web_scrapping_data_source_container import WebScrappingDataSourceContainer
from main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_standings_helper import WebScrappingStandingsHelper
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader


class WebScrappingStandingsOrchestratorService:

    def __init__(self, web_scrapping_data_source_container: WebScrappingDataSourceContainer):
        self.config_loader = ConfigLoader()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.web_scrapping_standings_helper = WebScrappingStandingsHelper(
            web_scrapping_data_source_container
        )

    def execute(self, standings_by_competitions_and_federation: Dict) -> Dict:
        return self.web_scrapping_standings_helper.get_standings_from_url(standings_by_competitions_and_federation)
