import logging
from time import sleep
from typing import Dict, Optional

import requests
from requests import ReadTimeout

from src.main.python.com.football.analyzer.data.domain.ports.http.http_requester_port import HttpRequesterPort


class HttpRequesterAdapter(HttpRequesterPort):

    def __init__(self, default_timeout: int = 30, default_headers: Optional[Dict[str, str]] = None):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.default_timeout = default_timeout
        self.default_headers = default_headers or {}

    def get_html_text(self, url: str) -> str:
        has_response = False
        response = None
        time_sleep = 1
        while has_response is False:
            try:
                response = requests.get(url, timeout=self.default_timeout, headers=self.default_headers)
                response.raise_for_status()
                has_response = True
            except ReadTimeout:
                sleep(time_sleep)
                time_sleep += 1
        return response.text
