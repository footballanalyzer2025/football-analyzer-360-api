from abc import ABC, abstractmethod


class HttpRequesterPort(ABC):

    @abstractmethod
    def get_html_text(self, url: str) -> str:
        pass
