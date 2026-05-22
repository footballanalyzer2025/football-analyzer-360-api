from bs4 import BeautifulSoup

from main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from main.python.com.football.analyzer.data.domain.ports.standings.standings_web_parser_port import StandingsWebParserPort


class FifaWorldCupStandingsWebParserAdapter(StandingsWebParserPort):
    def get_standings_in_html_soup(self, standings_table_html_soup: BeautifulSoup) -> dict:
        return {
            ConfigConstants.GENERAL_STANDING: self.get_standing(standings_table_html_soup)
        }

    @staticmethod
    def get_standing(standings_table_html_soup):
        standing = {}
        rows = standings_table_html_soup.find_all('tr', class_='ranking')
        for row in rows:
            td_position = row.find('td', class_='ranking-rank')
            td_country = row.find('td', class_='team-name')
            if td_position and td_country:
                standing[td_country.get_text(strip=True)] = int(td_position.get_text(strip=True))
        return standing
