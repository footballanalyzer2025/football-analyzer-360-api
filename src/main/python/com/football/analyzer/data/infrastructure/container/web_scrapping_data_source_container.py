from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.infrastructure.adapters.extractors.beautifulsoup_html_extractor_strategy import BeautifulSoupHTMLExtractorStrategy
from src.main.python.com.football.analyzer.data.infrastructure.adapters.http.http_requester_adapter import HttpRequesterAdapter
from src.main.python.com.football.analyzer.data.infrastructure.adapters.parsers.lxml_parser_adapter import LXMLParserAdapter


class WebScrappingDataSourceContainer:
    def __init__(self, timeout: int = 5, headers: dict = None):
        if headers is None:
            headers = ConfigConstants.HEADERS
        self.timeout = timeout
        self.headers = headers
        self.lxml_parser_adapter = LXMLParserAdapter()
        self.beautiful_soup_html_extractor_strategy = BeautifulSoupHTMLExtractorStrategy()
        self.http_requester_adapter = HttpRequesterAdapter(timeout, headers)

    def get_html_content(self, url: str) -> str:
        return self.http_requester_adapter.get_html_text(url)

    def parse_html(self, html_content: str):
        return self.lxml_parser_adapter.parse(html_content)

    def extract_text_by_selector_in_html_soup(self, html_soup, selector: str):
        return self.beautiful_soup_html_extractor_strategy.extract_element_text_strip_info(html_soup, selector)

    def extract_info_by_selector_in_html_soup(self, html_soup, selector: str):
        return self.beautiful_soup_html_extractor_strategy.extract_element_info(html_soup, selector)
    