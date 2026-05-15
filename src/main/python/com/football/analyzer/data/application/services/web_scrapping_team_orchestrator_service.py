from typing import Dict

from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_calendar_data_live_football_helper import WebScrappingCalendarDataLiveFootballHelper
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_main_data_live_football_helper import WebScrappingMainDataLiveFootballHelper
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_teams_data_live_football_helper import WebScrappingTeamsDataLiveFootballHelper


class WebScrappingTeamOrchestratorService:

    def __init__(self, web_scrapping_data_source_container, managers_data):
        self._config_loader = ConfigLoader()
        _main_helper = WebScrappingMainDataLiveFootballHelper(
            web_scrapping_data_source_container,
            self._config_loader
        )
        _calendar_helper = WebScrappingCalendarDataLiveFootballHelper(
            _main_helper,
            self._config_loader
        )
        self._team_helper = WebScrappingTeamsDataLiveFootballHelper(
            _main_helper,
            self._config_loader,
            managers_data
        )

    def execute(self, teams_data: Dict) -> Dict:
        return self._team_helper.get_teams_data(teams_data)
