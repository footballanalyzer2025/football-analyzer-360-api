from typing import List, Any

from src.main.python.com.football.analyzer.data.domain.ports.extractors.html_extractor_strategy import HTMLExtractorStrategy
from src.main.python.com.football.analyzer.data.infrastructure.adapters.exceptions.selector_syntax_error_exception import SelectorSyntaxErrorException


class BeautifulSoupHTMLExtractorStrategy(HTMLExtractorStrategy):

    def __init__(self):
        self.html_extractor_exception_handler = SelectorSyntaxErrorException()

    def extract_element_text_strip_info(self, html_soup, selector: str) -> List[str]:
        try:
            elements = html_soup.select(selector)
            return [element.text.strip() for element in elements]
        except Exception as exception:
            self.html_extractor_exception_handler.html_extractors_exception_handler(exception)
            raise

    def extract_element_info(self, html_soup, selector: str) -> List[Any]:
        try:
            return html_soup.select(selector)
        except Exception as exception:
            self.html_extractor_exception_handler.html_extractors_exception_handler(exception)
            raise
