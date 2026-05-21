import logging
from typing import Dict, List

from main.python.com.football.analyzer.data.infrastructure.container.web_scrapping_data_source_container import WebScrappingDataSourceContainer
from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_calendar_data_live_football_helper import WebScrappingCalendarDataLiveFootballHelper
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_main_data_live_football_helper import WebScrappingMainDataLiveFootballHelper


class WebScrappingCompetitionsByFederationsOrchestratorService:

    def __init__(self, web_scrapping_data_source_container: WebScrappingDataSourceContainer):
        self.config_loader = ConfigLoader()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.web_scrapping_data_source_container = web_scrapping_data_source_container
        self.main_helper = WebScrappingMainDataLiveFootballHelper(
            web_scrapping_data_source_container,
            self.config_loader
        )
        self.calendar_helper = WebScrappingCalendarDataLiveFootballHelper(
            self.main_helper,
            self.config_loader
        )

    def execute(self, competitions_by_federation: Dict) -> Dict:
        federations_data = self.get_federations_data(list(competitions_by_federation.keys()))
        result = {}
        for federation_name, competitions in competitions_by_federation.items():
            federation_url = self.get_federation_url(federation_name, federations_data)
            if not federation_url:
                self.logger.warning(f"⚠️ URL not found to '{federation_name}'")
                continue
            result[federation_name] = {
                ConfigConstants.MAIN_URL: federation_url,
                ConfigConstants.COMPETITIONS_DATA: {}
            }
            result[federation_name][ConfigConstants.COMPETITIONS_DATA] = self._process_federation_competitions(federation_url, competitions)
            self._process_competitions_sections(result[federation_name][ConfigConstants.COMPETITIONS_DATA])
        return result

    def get_federations_data(self, countries_and_federations_filter: List) -> Dict:
        return self.main_helper.get_main_data(
            self.config_loader.get_data_source_url(),
            self.config_loader.get_selector(ConfigConstants.COUNTRIES_OR_FEDERATIONS_SELECTOR),
            1,
            ConfigConstants.VALUE,
            countries_and_federations_filter,
            True
        )

    @staticmethod
    def get_federation_url(federation_name: str, federations_data: Dict) -> str:
        if federation_name in federations_data:
            return federations_data[federation_name].get(ConfigConstants.MAIN_URL, "")
        normalized_name = federation_name.strip()
        for name, data in federations_data.items():
            if name.strip() == normalized_name:
                return data.get(ConfigConstants.MAIN_URL, "")
        return ""

    def _process_federation_competitions(self, federation_url: str, competitions: List) -> Dict:
        competition_keys, competition_values = self.main_helper.get_data_filtered(
            federation_url,
            self.config_loader.get_selector(ConfigConstants.COMPETITIONS_SELECTOR),
            0,
            ConfigConstants.VALUE
        )
        all_competitions = dict(zip(competition_keys, competition_values))
        active_competitions_urls = {
            comp_name: comp_url
            for comp_name, comp_url in all_competitions.items()
            if comp_name in competitions
        }
        return self.main_helper.build_full_urls(active_competitions_urls)

    def _process_competitions_sections(self, competitions_data: Dict):
        for competition_name, competition_data in competitions_data.items():
            competition_sections = self.main_helper.get_main_data(
                competition_data[ConfigConstants.MAIN_URL],
                self.config_loader.get_selector(ConfigConstants.COMPETITIONS_SECTIONS_SELECTOR),
                0,
                ConfigConstants.HREF,
                self.config_loader.get_competitions_sections_filter(),
                True
            )
            self._enriched_competitions_data_with_calendar_section(competition_name, competition_sections, competitions_data)
            self._enriched_competitions_data_with_teams_section(competition_name, competition_sections, competitions_data)
            self._enriched_competitions_data_with_results_and_standings_section(competition_name, competition_sections, competitions_data)

    def _enriched_competitions_data_with_calendar_section(self, competition_name, competition_sections, competitions_data):
        calendar_section = self.config_loader.get_calendar_section()
        if calendar_section in competition_sections:
            competitions_data[competition_name][calendar_section] = {
                ConfigConstants.MATCHES: self.calendar_helper.get_calendar_data(
                    competition_sections[calendar_section][ConfigConstants.MAIN_URL],
                    competition_name
                )
            }

    def _enriched_competitions_data_with_teams_section(self, competition_name, competition_sections, competitions_data):
        teams_section = self.config_loader.get_teams_section()
        if teams_section in competition_sections:
            competitions_data[competition_name][teams_section] = self.main_helper.get_main_data(
                competition_sections[teams_section][ConfigConstants.MAIN_URL],
                self.config_loader.get_selector(ConfigConstants.TEAMS_SELECTOR),
                0,
                ConfigConstants.HREF,
                [],
                False
            )
            # if with_matches:
            #     competitions_data[competition_name][ConfigConstants.TEAMS_DATA] = self.teams_helper.get_teams_data(teams_data)

    def _enriched_competitions_data_with_results_and_standings_section(self, competition_name, competition_sections, competitions_data):
        results_and_standings_section = self.config_loader.get_results_and_standings_section()
        if results_and_standings_section in competition_sections:
            competitions_data[competition_name][results_and_standings_section] = competition_sections[results_and_standings_section]
