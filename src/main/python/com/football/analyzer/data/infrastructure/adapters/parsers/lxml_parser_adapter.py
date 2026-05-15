from bs4 import BeautifulSoup

from src.main.python.com.football.analyzer.data.domain.ports.parser.html_parser_port import HTMLParserPort

FEATURE_LXML = "lxml"


class LXMLParserAdapter(HTMLParserPort):

    def parse(self, html_content: str):
        if not html_content:
            return None

        if isinstance(html_content, str) and html_content.strip() == "":
            return None

        return BeautifulSoup(html_content, FEATURE_LXML)
