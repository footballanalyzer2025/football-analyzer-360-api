from abc import ABC, abstractmethod


class HTMLExtractorStrategy(ABC):

    @abstractmethod
    def extract_element_text_strip_info(self, html_soup, selector: str):
        pass

    @abstractmethod
    def extract_element_info(self, html_soup, selector: str):
        pass
