import logging
from typing import Dict, List

from main.python.com.football.analyzer.data.infrastructure.container.web_scrapping_data_source_container import WebScrappingDataSourceContainer
from main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_standings_helper import WebScrappingStandingsHelper
from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_calendar_data_live_football_helper import WebScrappingCalendarDataLiveFootballHelper
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_main_data_live_football_helper import WebScrappingMainDataLiveFootballHelper


class WebScrappingStandingsOrchestratorService:

    def __init__(self, web_scrapping_data_source_container: WebScrappingDataSourceContainer):
        self.config_loader = ConfigLoader()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.web_scrapping_data_source_container = web_scrapping_data_source_container
        self.main_helper = WebScrappingMainDataLiveFootballHelper(
            web_scrapping_data_source_container,
            self.config_loader
        )
        self.web_scrapping_standings_helper = WebScrappingStandingsHelper(
            web_scrapping_data_source_container
        )

    def execute(self, standings_by_competitions_and_federation: Dict) -> Dict:
        competition_name, standings_url = next(iter(standings_by_competitions_and_federation.items()))
        return self.web_scrapping_standings_helper.get_standings_from_url(competition_name, standings_url)
