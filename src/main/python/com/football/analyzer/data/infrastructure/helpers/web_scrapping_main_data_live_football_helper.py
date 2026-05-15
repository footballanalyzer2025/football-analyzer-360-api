from typing import Dict, List, Tuple

from bs4 import BeautifulSoup

from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader


class WebScrappingMainDataLiveFootballHelper:

    def __init__(self, container, config_loader: ConfigLoader):
        self._container = container
        self._config_loader = config_loader

    def get_main_data(
            self,
            data_source_url: str,
            selector: str,
            skip: int,
            element: str,
            filter_list: List,
            apply_filter: bool
    ) -> Dict:
        keys, values = self.get_data_filtered(data_source_url, selector, skip, element)
        filtered_data = self.apply_filter(dict(zip(keys, values)), filter_list, apply_filter)
        return self.build_full_urls(filtered_data)

    def get_data_filtered(
            self,
            data_source_url: str,
            selector: str,
            skip: int,
            element: str
    ) -> Tuple[List, List]:
        html_soup = self.get_html_soup(data_source_url)
        keys = self._container.extract_text_by_selector_in_html_soup(html_soup, selector)[skip:]
        options = self._container.extract_info_by_selector_in_html_soup(html_soup, selector)
        values = [option.get(element) for option in options if option.get(element)][skip:]
        return keys, values

    def get_html_soup(self, data_source_url: str) -> BeautifulSoup:
        html_content = self._container.get_html_content(data_source_url)
        return self._container.parse_html(html_content)

    @staticmethod
    def apply_filter(data_dict: Dict, filter_data: List, apply_filter: bool) -> Dict:
        if not apply_filter:
            return data_dict.copy()
        return {key: value for key, value in data_dict.items() if key in filter_data}

    def build_full_urls(self, relative_paths: Dict) -> Dict:
        base_url = self._config_loader.get_data_source_url().rstrip(ConfigConstants.SLASH)
        return {
            name: {
                ConfigConstants.MAIN_URL: self.get_full_clean_url(base_url, path)
            }
            for name, path in relative_paths.items()
        }

    @staticmethod
    def get_full_clean_url(base_url: str, path: str) -> str:
        clean_path = path if path.startswith(ConfigConstants.SLASH) else f"{ConfigConstants.SLASH}{path}"
        return f"{base_url}{clean_path}"
