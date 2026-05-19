import logging
from typing import Dict

from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_calendar_data_live_football_helper import WebScrappingCalendarDataLiveFootballHelper
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_main_data_live_football_helper import WebScrappingMainDataLiveFootballHelper
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_team_matches_data_live_football_helper import WebScrappingTeamMatchesDataLiveFootballHelper


class WebScrappingTeamsDataLiveFootballHelper:

    def __init__(
            self,
            main_helper: WebScrappingMainDataLiveFootballHelper,
            config_loader: ConfigLoader,
            managers_data
    ):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._managers_data = managers_data
        self._main_helper = main_helper
        self._config_loader = config_loader
        self._calendar_helper = WebScrappingCalendarDataLiveFootballHelper(
            self._main_helper,
            self._config_loader
        )
        self.team_matches_helper = WebScrappingTeamMatchesDataLiveFootballHelper(
            self._main_helper,
            self._calendar_helper,
            self._config_loader
        )

    def get_teams_data(self, teams_data: Dict) -> Dict:
        result = {}
        for team_name, team_data in teams_data.items():
            if team_name not in self._managers_data:
                result[team_name] = {
                    ConfigConstants.MAIN_URL: team_data[ConfigConstants.MAIN_URL],
                    ConfigConstants.HAS_MANAGER_DATA: False
                }
                continue
            team_sections = self._get_team_sections(team_data[ConfigConstants.MAIN_URL])
            dates_section = self._config_loader.get_dates_and_results_section()
            h2h_section = self._config_loader.get_h2h_section()
            result[team_name] = {
                ConfigConstants.MAIN_URL: team_data[ConfigConstants.MAIN_URL],
                ConfigConstants.HAS_MANAGER_DATA: True,
                ConfigConstants.MANAGER_START_DATE: self._managers_data[team_name],
                ConfigConstants.SECTIONS: {
                    dates_section: team_sections.get(dates_section, {}),
                    h2h_section: team_sections.get(h2h_section, {})
                }
            }
            result[team_name][ConfigConstants.MATCHES] = self.team_matches_helper.get_team_matches_data(
                team_name,
                result[team_name][ConfigConstants.SECTIONS][dates_section][ConfigConstants.MAIN_URL],
                self._managers_data[team_name]
            )
        return result

    def _get_team_sections(self, team_url: str) -> Dict:
        return self._main_helper.get_main_data(
            team_url,
            self._config_loader.get_selector(ConfigConstants.TEAMS_SECTIONS_SELECTOR),
            0,
            ConfigConstants.HREF,
            self._config_loader.get_teams_sections_filter(),
            True
        )
