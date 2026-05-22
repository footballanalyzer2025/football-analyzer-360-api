import logging
from typing import Dict, Any

from ..adapters.parsers.standings_web_parser_factory import StandingsWebParserFactory
from ..container.web_scrapping_data_source_container import WebScrappingDataSourceContainer
from ...commons.config.config_constants import ConfigConstants
from ...commons.config.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class WebScrappingStandingsHelper:

    def __init__(
            self,
            web_scrapping_data_source_container: WebScrappingDataSourceContainer
    ):
        self._config_loader = ConfigLoader()
        self._web_scrapping_data_source_container = web_scrapping_data_source_container
        self._competitions_types_config = self._config_loader.get_competitions_types_config()

    def get_standings_from_url(self, standings_by_competitions_and_federation: Dict) -> Dict[str, Any]:
        federation_name, competition_standings_url_data = next(iter(standings_by_competitions_and_federation.items()))
        if not federation_name or not competition_standings_url_data:
            logger.warning(f"No federation_name or competition standing url provided for competition")
            return {}
        competition_name, standings_url = next(iter(competition_standings_url_data.items()))
        if not competition_name or not standings_url:
            logger.warning(f"No competition or standings URL provided for competition in {federation_name}")
            return {}
        try:
            return self._get_standings_data(federation_name, competition_name, standings_url)
        except Exception as e:
            logger.error(f"Failed to scrape standings for {competition_name}: {e}")
            return {}

    def _get_standings_data(self, federation_name, competition_name, standings_url):
        standings_table_html_content = self._web_scrapping_data_source_container.get_html_content(standings_url)
        competition_type = self._get_competition_type(federation_name, competition_name)
        competition_type_section = self._config_loader.get_competition_type_section_at_ini(competition_type)
        standings_table_html_soup = self._web_scrapping_data_source_container.parse_html(standings_table_html_content).select_one(competition_type_section[ConfigConstants.LF_SELECTOR_STANDING])
        return StandingsWebParserFactory.get_parser(competition_type_section.name).get_standings_in_html_soup(standings_table_html_soup)

    def _get_competition_type(self, federation_name: str, competition_name: str):
        competition_type = None
        if ConfigConstants.FIFA == federation_name and ConfigConstants.WORLD_CUP == competition_name:
            competition_type = f'{ConfigConstants.FIFA}_{ConfigConstants.WORLD_CUP}'
        else:
            for competition_type_config in self._competitions_types_config:
                if f'{federation_name}-{competition_name}' in competition_type_config[ConfigConstants.COMPETITIONS].split(','):
                    competition_type = competition_type_config.name
                    break
        return competition_type
