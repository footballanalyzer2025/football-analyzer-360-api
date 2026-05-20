class ConfigConstants:

    # ========================================================================== #
    #                           KEYS IN CONFIG.INI                               #
    # ========================================================================== #
    #                              LIVE FOOTBALL                                 #
    # ========================================================================== #
    LIVE_FOOTBALL_INFORMATION = "LIVE_FOOTBALL_INFORMATION"
    URL_MAIN = "URL_MAIN"
    COUNTRIES_AND_FEDERATIONS = "COUNTRIES_AND_FEDERATIONS"
    COMPETITIONS_SECTIONS = "COMPETITIONS_SECTIONS"
    TEAMS_SECTION = "TEAMS_SECTION"
    CALENDAR_SECTION = "CALENDAR_SECTION"
    RESULTS_AND_STANDINGS_SECTION = "RESULTS_AND_STANDINGS_SECTION"
    TEAMS_SECTIONS = "TEAMS_SECTIONS"
    DATES_AND_RESULTS_SECTION = "DATES_AND_RESULTS_SECTION"
    H2H_SECTION = "H2H_SECTION"
    # ========================================================================== #
    #                    LIVE FOOTBALL FIFA (Special Case)                       #
    # ========================================================================== #
    FIFA = "FIFA"
    WORLD_RANKING_URL = "WORLD_RANKING_URL"

    # ========================================================================== #
    #                      SELECTORS KEYS IN CONFIG.INI                          #
    # ========================================================================== #
    LF_SELECTORS = "LF_SELECTORS"
    COUNTRIES_OR_FEDERATIONS_SELECTOR = "COUNTRIES_OR_FEDERATIONS"
    COMPETITIONS_SELECTOR = "COMPETITIONS"
    COMPETITIONS_SECTIONS_SELECTOR = "COMPETITIONS_SECTIONS"
    CALENDAR_GAME_PLAN_SELECTOR = "CALENDAR_GAME_PLAN"
    TEAMS_SELECTOR = "TEAMS"
    TEAMS_SECTIONS_SELECTOR = "TEAMS_SECTIONS"
    SESSIONS_SELECT_TEAM_SELECTOR = "SESSIONS_SELECT_TEAM"
    MATCHES_LIST_SELECTOR = "MATCHES_LIST"
    CLASS_SELECTOR = "class"
    ROW_CLASS_COMPETITION_HEAD_SELECTOR = "ROW_CLASS_COMPETITION_HEAD"
    ROW_CLASS_MATCH_SELECTOR = "ROW_CLASS_MATCH"
    ROW_TH_A_SELECTOR = "ROW_TH_A"
    ROW_TD_MATCH_DATE_SELECTOR = "ROW_TD_MATCH_DATE"
    ROW_TD_MATCH_RESULT_ALL_SELECTOR = "ROW_TD_MATCH_RESULT_ALL"
    ROW_TD_MATCH_RESULT_ALL_A_SELECTOR = "ROW_TD_MATCH_RESULT_ALL_A"
    ROW_TD_MATCH_RESULT_TENDENCY_SELECTOR = "ROW_TD_MATCH_RESULT_TENDENCY"
    ROW_TD_MATCH_VENUE_SELECTOR = "ROW_TD_MATCH_VENUE"
    ROW_TD_TEAM_SHORTNAME_EXTENDED_A_SELECTOR = "ROW_TD_MATCH_SHORTNAME_EXTENDED_A"
    STATUS_MATCH_FINISHED_SELECTOR = "STATUS_MATCH_FINISHED"
    STATUS_MATCH_UPCOMING_SELECTOR = "STATUS_MATCH_UPCOMING"
    STATUS_MATCH_TO_ANALYZE = "STATUS_MATCH_TO_ANALYZE"

    # ========================================================================== #
    #                      KEYS COMPETITIONS AND MATCHES                         #
    # ========================================================================== #
    COMPETITIONS_DATA = 'competitions_data'
    COMPETITIONS_BY_FEDERATION = 'competitions_by_federation'
    DATE_FORMAT_WITH_PERIODS = '%d.%m.%Y'
    HAS_MANAGER_DATA = 'has_manager_data'
    HREF = 'href'
    MAIN_URL = 'main_url'
    MANAGER_START_DATE = 'manager_start_date'
    MATCHES = 'matches'
    SECTIONS = 'sections'
    SLASH = '/'
    TEAMS_DATA = 'teams_data'
    TEAMS_IN_COMPETITION = 'teams_in_competition'
    VALUE = 'value'
    NUMBER_OF_TEAMS = 'number_of_teams'
    UPCOMING_MATCHES = 'upcoming_matches'
    TOTAL_UPCOMING = 'total_upcoming'
    LIMIT_APPLIED = 'limit_applied'

    ALL_MATCHES = 'all_matches'
    AWAY_TEAM = 'away_team'
    COMPETITION_NAME = "competition_name"
    DATE = 'date'
    EXTRA_TIME = 'extra_time'
    FIRST_HALF = 'first_half'
    FULL_EXTRA_TIME = 'full_extra_time'
    FULL_TIME = 'full_time'
    FULL_RESULT = 'full_result'
    WAS_CANCELED = 'was_canceled'
    HAS_EXTRA_TIME = 'has_extra_time'
    HAS_PENALTIES = 'has_penalties'
    HOME_TEAM = 'home_team'
    MATCH_LINK = 'match_link'
    NAME = 'name'
    NONE_RESULTS = ('-:-', '-:-apla.', '-:-n.d.', '-:--:-anu.')
    OPPONENT = 'opponent'
    PENALTIES = 'penalties'
    RESULT = 'result'
    RESULT_TENDENCY = 'result_tendency'
    STATUS = 'status'
    SECOND_HALF = 'second_half'
    TWO_PERIODS = ':'
    VENUE = 'venue'
    TEAM_NAME = 'team_name'
    TEAM_MATCHES = 'team_matches'
    CREATED_AT = 'created_at'
    UPDATE_AT = 'updated_at'

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
    }

    # ========================================================================== #
    #                                  TELEGRAM                                  #
    # ========================================================================== #
    TELEGRAM = 'TELEGRAM'
    TOKEN = 'TOKEN'
    CHAT_ID = 'CHAT_ID'

    # ========================================================================== #
    #                                REQUESTS BODY                               #
    # ========================================================================== #

    CALENDARS_BY_FEDERATION_AND_COMPETITIONS = "calendars_by_federation_and_competitions"
    STATS_BY_FEDERATION_AND_COMPETITIONS = "stats_by_federation_and_competitions"
