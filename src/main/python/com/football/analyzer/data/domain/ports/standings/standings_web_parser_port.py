from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List


class StandingsWebParserPort(ABC):
    @abstractmethod
    def get_standings_in_html_soup(self, standings_table_html_soup: BeautifulSoup) -> List:
        pass
