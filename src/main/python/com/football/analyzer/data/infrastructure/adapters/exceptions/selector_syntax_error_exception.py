import logging

from soupsieve import SelectorSyntaxError

from src.main.python.com.football.analyzer.data.infrastructure.adapters.exceptions.html_extractor_exception_handler import HTMLExtractorExceptionHandler

logger = logging.getLogger(__name__)


class SelectorSyntaxErrorException(HTMLExtractorExceptionHandler):

    def html_extractors_exception_handler(self, exception):
        if isinstance(exception, SelectorSyntaxError):
            logger.error("[Error] SelectorSyntaxError:", exception)
        else:
            super().html_extractors_exception_handler(exception)
