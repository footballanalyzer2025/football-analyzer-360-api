from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_ini import ConfigIni
from src.main.python.com.football.analyzer.data.commons.config.singleton_meta import SingletonMeta


class ConfigLoader(metaclass=SingletonMeta):

    def __init__(self):
        self.config_ini = ConfigIni()
        self.all_config_ini = self.config_ini.config_parser()
        self.constants = ConfigConstants

    def get_data_source_url(self) -> str:
        return self.all_config_ini[self.constants.LIVE_FOOTBALL_INFORMATION][self.constants.URL_MAIN]

    def get_teams_section(self) -> str:
        return self.all_config_ini[self.constants.LIVE_FOOTBALL_INFORMATION][self.constants.TEAMS_SECTION]

    def get_calendar_section(self) -> str:
        return self.all_config_ini[self.constants.LIVE_FOOTBALL_INFORMATION][self.constants.CALENDAR_SECTION]

    def get_results_and_standings_section(self) -> str:
        return self.all_config_ini[self.constants.LIVE_FOOTBALL_INFORMATION][self.constants.RESULTS_AND_STANDINGS_SECTION]

    def get_dates_and_results_section(self) -> str:
        return self.all_config_ini[self.constants.LIVE_FOOTBALL_INFORMATION][self.constants.DATES_AND_RESULTS_SECTION]

    def get_h2h_section(self) -> str:
        return self.all_config_ini[self.constants.LIVE_FOOTBALL_INFORMATION][self.constants.H2H_SECTION]

    def get_selector(self, selector_name: str) -> str:
        return self.all_config_ini[self.constants.LF_SELECTORS][selector_name]

    def get_countries_and_federations_filter(self) -> list:
        filter_str = self.all_config_ini[self.constants.LIVE_FOOTBALL_INFORMATION][self.constants.COUNTRIES_AND_FEDERATIONS]
        return [item.strip() for item in filter_str.split(',') if item.strip()]

    def get_competitions_sections_filter(self) -> list:
        filter_str = self.all_config_ini[self.constants.LIVE_FOOTBALL_INFORMATION][self.constants.COMPETITIONS_SECTIONS]
        return [item.strip() for item in filter_str.split(',') if item.strip()]

    def get_teams_sections_filter(self) -> list:
        filter_str = self.all_config_ini[self.constants.LIVE_FOOTBALL_INFORMATION][self.constants.TEAMS_SECTIONS]
        return [item.strip() for item in filter_str.split(',') if item.strip()]

    def get_fifa_world_ranking_url_special_case(self) -> str:
        return self.all_config_ini[f'{self.constants.FIFA}_{self.constants.WORLD_CUP}'][self.constants.WORLD_RANKING_URL]

    def get_fifa_world_ranking_file_special_case(self) -> str:
        return self.all_config_ini[f'{self.constants.FIFA}_{self.constants.WORLD_CUP}'][self.constants.WORLD_RANKING_FILE_PATH]

    def get_competitions_types_config(self):
        all_sections = self.all_config_ini.sections()
        return [self.all_config_ini[section] for section in all_sections if section.startswith(self.constants.LF_COMPETITION_TYPE_)]

    def get_competition_type_section_at_ini(self, key):
        return self.all_config_ini[key]

    def get_analyzer_matches_path(self):
        return self.all_config_ini[ConfigConstants.ANALYZERS_FILES][ConfigConstants.ANALYZER_MATCHES_PATH]

    def get_telegram_config(self) -> dict:
        return {
            self.constants.TOKEN: self.all_config_ini[self.constants.TELEGRAM][self.constants.TOKEN],
            self.constants.CHAT_ID: self.all_config_ini[self.constants.TELEGRAM][self.constants.CHAT_ID]
        }
