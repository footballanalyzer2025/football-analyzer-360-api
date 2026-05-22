import logging
from typing import Dict, Any

from ..container.web_scrapping_data_source_container import WebScrappingDataSourceContainer

logger = logging.getLogger(__name__)


class WebScrappingStandingsHelper:

    def __init__(
            self,
            web_scrapping_data_source_container: WebScrappingDataSourceContainer
    ):
        self._web_scrapping_data_source_container = web_scrapping_data_source_container

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
            standings_table_html_content = self._web_scrapping_data_source_container.get_html_content(standings_url)
            standings_table_html_soup = self._web_scrapping_data_source_container.parse_html(standings_table_html_content).select_one('table.module-ranking')
            if not standings_table_html_soup:
                return {}
            standings = self.get_standings_in_html_soup(standings_table_html_soup)
            row_data = {
                "Standings": standings
            }
            return self._parse_standings_by_format(federation_name, competition_name, row_data)
        except Exception as e:
            logger.error(f"Failed to scrape standings for {competition_name}: {e}")
            return {}

    @staticmethod
    def get_standings_in_html_soup(standings_table_html_soup):
        rows = standings_table_html_soup.find_all('tr', class_='ranking')
        standings = []
        for row in rows:
            td_position = row.find('td', class_='ranking-rank')
            td_country = row.find('td', class_='team-name')
            if td_position and td_country:
                standings.append((td_position.get_text(strip=True), td_country.get_text(strip=True)))
        return standings

    @staticmethod
    def _parse_standings_by_format(federation_name: str, competition_name: str, raw_data: Dict) -> Dict[str, Any]:
        return {
            "federation": federation_name,
            "competition": competition_name,
            "raw_data": raw_data
        }
