from typing import Dict

from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_calendar_data_live_football_helper import WebScrappingCalendarDataLiveFootballHelper
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_main_data_live_football_helper import WebScrappingMainDataLiveFootballHelper
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_team_matches_data_live_football_helper import WebScrappingTeamMatchesDataLiveFootballHelper


class WebScrappingTeamMatchesOrchestratorService:

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
        self._team_matches_helper = WebScrappingTeamMatchesDataLiveFootballHelper(
            _main_helper,
            _calendar_helper,
            self._config_loader,
            managers_data
        )
        self._managers_data = managers_data

    def execute(self, teams_data: Dict) -> Dict:
        result = {}
        for team_name, team_data in teams_data.items():
            result[team_name] = team_data
            if ConfigConstants.SECTIONS in team_data:
                result[team_name][ConfigConstants.MATCHES] = self._team_matches_helper.get_team_matches_data(
                    team_data[ConfigConstants.SECTIONS][self._config_loader.get_dates_and_results_section()][ConfigConstants.MAIN_URL],
                    self._managers_data[team_name]
                )
        return result
