from datetime import datetime
from typing import Dict, List, Optional

from bs4 import Tag

from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_main_data_live_football_helper import WebScrappingMainDataLiveFootballHelper


class WebScrappingCalendarDataLiveFootballHelper:

    def __init__(self, main_helper: WebScrappingMainDataLiveFootballHelper, config_loader: ConfigLoader):
        self._main_helper = main_helper
        self._config_loader = config_loader

    def get_calendar_data(self, calendar_url: str, competition_name: str) -> Dict:
        html_soup = self._main_helper.get_html_soup(calendar_url)
        calendar_container = html_soup.select_one(
            self._config_loader.get_selector(ConfigConstants.CALENDAR_GAME_PLAN_SELECTOR)
        )
        if not calendar_container:
            return {}
        inner_container = calendar_container.find("div")
        if not inner_container:
            inner_container = calendar_container
        calendar_data = {}
        all_matches = []
        current_heading = None
        for element in inner_container.children:
            if not hasattr(element, 'name'):
                continue
            if isinstance(element, Tag):
                if self._is_heading_element(element):
                    current_heading = self._extract_heading_text(element)
                    if current_heading not in calendar_data:
                        calendar_data[current_heading] = []
                elif self._is_match_element(element) and current_heading:
                    match_data = self._extract_match_from_calendar(element, competition_name)
                    if match_data:
                        calendar_data[current_heading].append(match_data)
                        all_matches.append(match_data)
        all_matches.sort(key=lambda x: datetime.strptime(
            x[ConfigConstants.DATE],
            ConfigConstants.DATE_FORMAT_WITH_PERIODS
        ))
        calendar_data[ConfigConstants.ALL_MATCHES] = all_matches
        return calendar_data

    @staticmethod
    def _is_heading_element(element: Tag) -> bool:
        element_class = element.get(ConfigConstants.CLASS_SELECTOR)
        heading_classes = ['round-head', 'hs-head--round']
        return any(cls in element_class for cls in heading_classes)

    @staticmethod
    def _is_match_element(element: Tag) -> bool:
        element_class = element.get(ConfigConstants.CLASS_SELECTOR)
        return 'match' in element_class

    @staticmethod
    def _extract_heading_text(element: Tag) -> str:
        return element.get_text(strip=True)

    def _extract_match_from_calendar(self, match_element: Tag, competition_name: str) -> Optional[Dict]:
        date_element = match_element.find_previous_sibling(class_='match-date')
        match_date = date_element.get_text(strip=True) if date_element else ""
        home_team = self._get_team_name(match_element, 'team-name-home')
        away_team = self._get_team_name(match_element, 'team-name-away')
        result_tag = match_element.find(class_='match-result')
        result = self.parse_match_result(result_tag, home_team, away_team) if result_tag else {}
        match_link_tag = None
        if result_tag:
            match_link_tag = result_tag.find('a')
        match_path = match_link_tag.get(ConfigConstants.HREF) if match_link_tag else ""
        match_url = self._main_helper.get_full_clean_url(
            self._config_loader.get_data_source_url().rstrip(ConfigConstants.SLASH),
            match_path
        ) if match_path else ""
        element_class = match_element.get(ConfigConstants.CLASS_SELECTOR)
        is_finished = ConfigConstants.STATUS_MATCH_FINISHED_SELECTOR in element_class
        is_upcoming = ConfigConstants.STATUS_MATCH_UPCOMING_SELECTOR in element_class
        status = self._determine_match_status(is_finished, is_upcoming, match_link_tag)
        return {
            ConfigConstants.DATE: match_date,
            ConfigConstants.HOME_TEAM: home_team,
            ConfigConstants.AWAY_TEAM: away_team,
            ConfigConstants.RESULT: result,
            ConfigConstants.MATCH_LINK: match_url,
            ConfigConstants.STATUS: status,
            ConfigConstants.COMPETITION_NAME: competition_name
        }

    @staticmethod
    def _get_team_name(match_element, class_value):
        team_element = match_element.find(class_=class_value)
        return team_element.get_text(strip=True) if team_element else ""

    def _determine_match_status(self, is_finished: bool, is_upcoming: bool, match_link_tag) -> str:
        if is_finished:
            return self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_FINISHED_SELECTOR)
        if is_upcoming:
            return self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_UPCOMING_SELECTOR)
        return self._determine_fallback_status(match_link_tag)

    def _determine_fallback_status(self, match_link_tag) -> str:
        if match_link_tag is None:
            return self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_UPCOMING_SELECTOR)
        if match_link_tag.text and match_link_tag.text == '-:-':
            return self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_UPCOMING_SELECTOR)
        return self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_FINISHED_SELECTOR)

    def parse_match_result(self, result_match_data: Tag, left_team: str, right_team: str) -> Dict:
        result = self._init_result(left_team, right_team)
        text = result_match_data.text.strip()
        if text in ConfigConstants.NONE_RESULTS:
            return result
        spans = result_match_data.find_all('span', class_='match-incident')
        if any('canc.' in span.text for span in spans):
            result[ConfigConstants.WAS_CANCELED] = True
        has_extra_time = any('pró.' in span.text for span in spans)
        has_penalties = any('pn.' in span.text for span in spans)
        a_tags = result_match_data.find_all('a')
        scores_by_period_list = [tag.text.strip().split(ConfigConstants.TWO_PERIODS) for tag in a_tags]
        if not a_tags:
            return result
        if has_penalties:
            return self._parse_penalties_match(result, scores_by_period_list, left_team, right_team)
        if has_extra_time:
            return self._parse_extra_time_match(result, scores_by_period_list, left_team, right_team)
        return self._parse_normal_match(result, scores_by_period_list, left_team, right_team)

    @staticmethod
    def _init_result(left_team: str, right_team: str):
        return {
            ConfigConstants.FIRST_HALF: {left_team: 0, right_team: 0},
            ConfigConstants.SECOND_HALF: {left_team: 0, right_team: 0},
            ConfigConstants.FULL_TIME: {left_team: 0, right_team: 0},
            ConfigConstants.WAS_CANCELED: False,
            ConfigConstants.HAS_EXTRA_TIME: False,
            ConfigConstants.EXTRA_TIME: {left_team: 0, right_team: 0},
            ConfigConstants.FULL_EXTRA_TIME: {left_team: 0, right_team: 0},
            ConfigConstants.HAS_PENALTIES: False,
            ConfigConstants.PENALTIES: {left_team: 0, right_team: 0}
        }

    def _parse_penalties_match(self, result: Dict, scores_by_period_list: List, left_team: str, right_team: str) -> Dict:
        result[ConfigConstants.HAS_PENALTIES] = True
        result[ConfigConstants.PENALTIES] = self._get_score_at_period(scores_by_period_list[0], left_team, right_team)
        if len(scores_by_period_list) == 4:
            result[ConfigConstants.HAS_EXTRA_TIME] = True
            return self._parse_penalties_with_extra_time(result, scores_by_period_list, left_team, right_team)
        if len(scores_by_period_list) == 3:
            return self._parse_penalties_without_extra_time(result, scores_by_period_list, left_team, right_team)
        return result

    def _parse_penalties_with_extra_time(self, result: Dict, scores_by_period_list: List, left_team: str, right_team: str) -> Dict:
        result[ConfigConstants.FIRST_HALF] = self._get_score_at_period(scores_by_period_list[1], left_team, right_team)
        result[ConfigConstants.FULL_TIME] = self._get_score_at_period(scores_by_period_list[2], left_team, right_team)
        result[ConfigConstants.SECOND_HALF] = self._get_score_calculate_at_period(result, ConfigConstants.FULL_TIME, ConfigConstants.FIRST_HALF, left_team, right_team)
        result[ConfigConstants.FULL_EXTRA_TIME] = self._get_score_at_period(scores_by_period_list[3], left_team, right_team)
        result[ConfigConstants.EXTRA_TIME] = self._get_score_calculate_at_period(result, ConfigConstants.FULL_EXTRA_TIME, ConfigConstants.FULL_TIME, left_team, right_team)
        return result

    def _parse_penalties_without_extra_time(self, result: Dict, scores_by_period_list: List, left_team: str, right_team: str) -> Dict:
        result[ConfigConstants.FIRST_HALF] = self._get_score_at_period(scores_by_period_list[1], left_team, right_team)
        result[ConfigConstants.FULL_TIME] = self._get_score_at_period(scores_by_period_list[2], left_team, right_team)
        result[ConfigConstants.SECOND_HALF] = self._get_score_calculate_at_period(result, ConfigConstants.FULL_TIME, ConfigConstants.FIRST_HALF, left_team, right_team)
        return result

    def _parse_extra_time_match(self, result: Dict, scores_by_period_list: List, left_team: str, right_team: str) -> Dict:
        result[ConfigConstants.HAS_EXTRA_TIME] = True
        if len(scores_by_period_list) >= 3:
            result[ConfigConstants.FIRST_HALF] = self._get_score_at_period(scores_by_period_list[1], left_team, right_team)
            result[ConfigConstants.FULL_TIME] = self._get_score_at_period(scores_by_period_list[2], left_team, right_team)
            result[ConfigConstants.SECOND_HALF] = self._get_score_calculate_at_period(result, ConfigConstants.FULL_TIME, ConfigConstants.FIRST_HALF, left_team, right_team)
            if len(scores_by_period_list) >= 4:
                result[ConfigConstants.FULL_EXTRA_TIME] = self._get_score_at_period(scores_by_period_list[0], left_team, right_team)
                result[ConfigConstants.EXTRA_TIME] = self._get_score_at_period(scores_by_period_list[3], left_team, right_team)
            else:
                result[ConfigConstants.FULL_EXTRA_TIME] = self._get_score_at_period(scores_by_period_list[0], left_team, right_team)
                result[ConfigConstants.EXTRA_TIME] = self._get_score_calculate_at_period(result, ConfigConstants.FULL_EXTRA_TIME, ConfigConstants.FULL_TIME, left_team, right_team)
        return result

    def _parse_normal_match(self, result: Dict, scores_by_period_list: List, left_team: str, right_team: str) -> Dict:
        if len(scores_by_period_list) >= 2:
            result[ConfigConstants.FIRST_HALF] = self._get_score_at_period(scores_by_period_list[1], left_team, right_team)
            result[ConfigConstants.FULL_TIME] = self._get_score_at_period(scores_by_period_list[0], left_team, right_team)
            result[ConfigConstants.SECOND_HALF] = self._get_score_calculate_at_period(result, ConfigConstants.FULL_TIME, ConfigConstants.FIRST_HALF, left_team, right_team)
        elif len(scores_by_period_list) == 1:
            result[ConfigConstants.FULL_TIME] = self._get_score_at_period(scores_by_period_list[0], left_team, right_team)
        return result

    @staticmethod
    def _get_score_at_period(period_time: List, left_team: str, right_team: str):
        return {
            left_team: int(period_time[0]) if len(period_time) > 0 else 0,
            right_team: int(period_time[1]) if len(period_time) > 1 else 0
        }

    @staticmethod
    def _get_score_calculate_at_period(result: Dict, full_time_type: str, first_half_time_type: str, left_team: str, right_team: str):
        return {
            left_team: result[full_time_type][left_team] - result[first_half_time_type][left_team],
            right_team: result[full_time_type][right_team] - result[first_half_time_type][right_team]
        }
