from bs4 import BeautifulSoup
from typing import List

from main.python.com.football.analyzer.data.domain.ports.standings.standings_web_parser_port import StandingsWebParserPort


class FifaWorldCupStandingsWebParserAdapter(StandingsWebParserPort):
    def get_standings_in_html_soup(self, standings_table_html_soup: BeautifulSoup) -> List:
        rows = standings_table_html_soup.find_all('tr', class_='ranking')
        standings = []
        for row in rows:
            td_position = row.find('td', class_='ranking-rank')
            td_country = row.find('td', class_='team-name')
            if td_position and td_country:
                standings.append((td_position.get_text(strip=True), td_country.get_text(strip=True)))
        return standings
