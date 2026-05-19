import logging
from datetime import datetime
from typing import Dict, List, Optional

from bs4 import Tag

from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_calendar_data_live_football_helper import WebScrappingCalendarDataLiveFootballHelper
from src.main.python.com.football.analyzer.data.infrastructure.helpers.web_scrapping_main_data_live_football_helper import WebScrappingMainDataLiveFootballHelper


class WebScrappingTeamMatchesDataLiveFootballHelper:

    def __init__(
            self,
            main_helper: WebScrappingMainDataLiveFootballHelper,
            calendar_helper: WebScrappingCalendarDataLiveFootballHelper,
            config_loader: ConfigLoader
    ):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._main_helper = main_helper
        self._calendar_helper = calendar_helper
        self._config_loader = config_loader

    def get_team_matches_data(self, team_name: str, team_matches_url: str, manager_start_date: str) -> Dict:
        all_sessions = self._main_helper.get_main_data(
            team_matches_url,
            self._config_loader.get_selector(ConfigConstants.SESSIONS_SELECT_TEAM_SELECTOR),
            0,
            ConfigConstants.VALUE,
            [],
            False
        )
        if not all_sessions:
            return {}
        first_session = next(iter(all_sessions))
        sessions_filter = self._get_season_filter(first_session, manager_start_date)
        filtered_sessions = self._main_helper.apply_filter(all_sessions, sessions_filter, True)
        return self._get_games_by_team_data(team_name, filtered_sessions)

    @staticmethod
    def _get_season_filter(session_type: str, init_date: str) -> List:
        init_dt = datetime.strptime(init_date, ConfigConstants.DATE_FORMAT_WITH_PERIODS)
        if ConfigConstants.SLASH in session_type:
            end_year = int(session_type.split(ConfigConstants.SLASH)[0])
            current_start = init_dt.year if init_dt.month > 6 else init_dt.year - 1
            return [f"{year}{ConfigConstants.SLASH}{year + 1}" for year in range(current_start, end_year + 1)]
        end_year = int(session_type)
        return [str(year) for year in range(init_dt.year, end_year + 1)]

    def _get_games_by_team_data(self, team_name: str, sessions_by_team_full_url_filtered: Dict) -> Dict:
        games_by_team_data = {}
        for session, session_data in sessions_by_team_full_url_filtered.items():
            all_rows = self._main_helper.get_html_soup(session_data[ConfigConstants.MAIN_URL]).select(
                self._config_loader.get_selector(ConfigConstants.MATCHES_LIST_SELECTOR)
            )
            self._process_match_rows(team_name, all_rows, session, games_by_team_data)
        all_matches = []
        for sessions_by_competition in games_by_team_data.values():
            for matches_at_session in sessions_by_competition.values():
                all_matches.extend(matches_at_session)
        all_matches.sort(
            key=lambda x: datetime.strptime(x[ConfigConstants.DATE], ConfigConstants.DATE_FORMAT_WITH_PERIODS),
            reverse=True
        )
        games_by_team_data[ConfigConstants.ALL_MATCHES] = all_matches
        return games_by_team_data

    def _process_match_rows(self, team_name: str, all_rows: List[Tag], session: str, games_by_team_data: Dict) -> None:
        current_tournament = None
        for row in all_rows:
            row_class = row.get(self._config_loader.get_selector(ConfigConstants.CLASS_SELECTOR))
            if self._is_competition_head_row(row_class):
                current_tournament = self._extract_tournament_name(row)
                self._initialize_tournament_session(games_by_team_data, current_tournament, session)
            elif self._is_match_row(row_class) and current_tournament:
                self._add_match_to_tournament(team_name, games_by_team_data, current_tournament, session, row)

    def _is_competition_head_row(self, row_class: List) -> bool:
        return self._config_loader.get_selector(ConfigConstants.ROW_CLASS_COMPETITION_HEAD_SELECTOR) in row_class

    def _extract_tournament_name(self, row: Tag) -> str:
        selector = self._config_loader.get_selector(ConfigConstants.ROW_TH_A_SELECTOR)
        tournaments_heads = row.select(selector)
        element = tournaments_heads[0]
        if not element.text.strip() and len(tournaments_heads) > 0:
            element = tournaments_heads[1]
        return element.text.strip() if element else ""

    @staticmethod
    def _initialize_tournament_session(games_by_team_data: Dict, tournament: str, session: str) -> None:
        if tournament not in games_by_team_data:
            games_by_team_data[tournament] = {}
        if session not in games_by_team_data[tournament]:
            games_by_team_data[tournament][session] = []

    def _is_match_row(self, row_class: List) -> bool:
        return self._config_loader.get_selector(ConfigConstants.ROW_CLASS_MATCH_SELECTOR) in row_class

    def _add_match_to_tournament(
            self,
            team_name: str,
            games_by_team_data: Dict,
            tournament: str,
            session: str,
            row: Tag
    ) -> None:
        if session not in games_by_team_data[tournament]:
            games_by_team_data[tournament][session] = []
        match_data = self._extract_match_data(team_name, row, tournament)
        if match_data:
            games_by_team_data[tournament][session].append(match_data)

    def _extract_match_data(self, team_name: str, row: Tag, tournament: str) -> Optional[Dict]:
        selectors = self._get_match_selectors()
        match_date = row.select_one(selectors[ConfigConstants.DATE])
        venue_tag = row.select_one(selectors[ConfigConstants.VENUE])
        venue = venue_tag.text.strip() if venue_tag else ""
        opponent = self._get_opponent(row, selectors)
        result_tag = row.select_one(selectors[ConfigConstants.RESULT])
        match_result = self._calendar_helper.parse_match_result(result_tag, team_name, opponent) if result_tag else {}
        match_link = row.select_one(selectors[ConfigConstants.MATCH_LINK])
        row_class = row.get(self._config_loader.get_selector(ConfigConstants.CLASS_SELECTOR))
        is_finished = self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_FINISHED_SELECTOR) in row_class
        match_path = match_link.get(ConfigConstants.HREF) if match_link else ""
        return {
            ConfigConstants.DATE: match_date.text.strip() if match_date else "",
            ConfigConstants.VENUE: venue,
            ConfigConstants.OPPONENT: opponent,
            ConfigConstants.RESULT: match_result,
            ConfigConstants.MATCH_LINK: self._main_helper.get_full_clean_url(
                self._config_loader.get_data_source_url().rstrip(ConfigConstants.SLASH),
                match_path
            ),
            ConfigConstants.STATUS: self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_FINISHED_SELECTOR) if is_finished
            else self._config_loader.get_selector(ConfigConstants.STATUS_MATCH_UPCOMING_SELECTOR),
            ConfigConstants.COMPETITION_NAME: tournament
        }

    def _get_match_selectors(self) -> Dict:
        return {
            ConfigConstants.DATE: self._config_loader.get_selector(ConfigConstants.ROW_TD_MATCH_DATE_SELECTOR),
            ConfigConstants.VENUE: self._config_loader.get_selector(ConfigConstants.ROW_TD_MATCH_VENUE_SELECTOR),
            ConfigConstants.OPPONENT: self._config_loader.get_selector(ConfigConstants.ROW_TD_TEAM_SHORTNAME_EXTENDED_A_SELECTOR),
            ConfigConstants.RESULT: self._config_loader.get_selector(ConfigConstants.ROW_TD_MATCH_RESULT_ALL_SELECTOR),
            ConfigConstants.RESULT_TENDENCY: self._config_loader.get_selector(ConfigConstants.ROW_TD_MATCH_RESULT_TENDENCY_SELECTOR),
            ConfigConstants.MATCH_LINK: self._config_loader.get_selector(ConfigConstants.ROW_TD_MATCH_RESULT_ALL_A_SELECTOR)
        }

    @staticmethod
    def _get_opponent(row, selectors):
        opponent = row.select_one(selectors[ConfigConstants.OPPONENT])
        return opponent.text.strip() if opponent else ""
