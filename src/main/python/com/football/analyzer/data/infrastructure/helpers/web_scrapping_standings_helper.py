import logging
from typing import Dict, Any

from .competition_type_helper import CompetitionTypeHelper
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
        self._competition_type_helper = CompetitionTypeHelper()

    def get_standings_from_url(self, standings_by_competitions_and_federation: Dict) -> Dict[str, Any]:
        federation_name, competition_standings_url_data = next(iter(standings_by_competitions_and_federation.items()))
        if not federation_name or not competition_standings_url_data:
            return {}
        competition_name, standings_url = next(iter(competition_standings_url_data.items()))
        if not competition_name or not standings_url:
            return {}
        try:
            return self._get_standings_data(federation_name, competition_name, standings_url)
        except KeyError:
            return {}

    def _get_standings_data(self, federation_name, competition_name, standings_url):
        standings_table_html_content = self._web_scrapping_data_source_container.get_html_content(standings_url)
        competition_type = self._competition_type_helper.get_competition_type(federation_name, competition_name)
        competition_type_section = self._config_loader.get_competition_type_section_at_ini(competition_type)
        standings_table_html_soup = self._web_scrapping_data_source_container.parse_html(standings_table_html_content).select_one(competition_type_section[ConfigConstants.LF_SELECTOR_STANDING])
        return StandingsWebParserFactory.get_parser(competition_type_section.name).get_standings_in_html_soup(standings_table_html_soup)
