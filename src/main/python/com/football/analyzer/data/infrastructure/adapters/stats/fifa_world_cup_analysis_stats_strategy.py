from typing import Dict, Any

from main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from main.python.com.football.analyzer.data.domain.ports.stats.analysis_stats_strategy import AnalysisStatsStrategy

TEAMS_MISSING_FROM_THE_RANKING_FIFA = {
    'Bosnia y Hercegovina': 65,
    'Curazao': 82,
    'Nueva Zelanda': 85
}


class FifaWorldCupAnalysisStatsStrategy(AnalysisStatsStrategy):
    def execute(self, match_to_analyze: Dict[str, Any], all_teams: Dict[str, Dict[str, Any]], all_standings_competition: Dict):
        home_team_data_to_analyze = self._get_team_data_to_analyze(ConfigConstants.HOME_TEAM, all_standings_competition, all_teams, match_to_analyze)
        away_team_data_to_analyze = self._get_team_data_to_analyze(ConfigConstants.AWAY_TEAM, all_standings_competition, all_teams, match_to_analyze)
        print("OK")

    def _get_team_data_to_analyze(self, venue_team, all_standings_competition, all_teams, match_to_analyze) -> Dict:
        team_name = match_to_analyze[venue_team]
        ranking_fifa = all_standings_competition[ConfigConstants.GENERAL_STANDING]
        self._update_ranking_fifa(team_name, ranking_fifa)
        team_matches = all_teams[match_to_analyze[venue_team]][ConfigConstants.MATCHES][ConfigConstants.ALL_MATCHES]
        return {
            team_name: {
                ConfigConstants.POSITION: ranking_fifa[team_name],
                ConfigConstants.OPPONENTS_DATA: self._get_standings_sorted_opponents(ranking_fifa, team_matches, team_name)
            }
        }

    @staticmethod
    def _update_ranking_fifa(team_name, ranking_fifa):
        if team_name not in ranking_fifa and team_name in TEAMS_MISSING_FROM_THE_RANKING_FIFA:
            ranking_fifa[team_name] = TEAMS_MISSING_FROM_THE_RANKING_FIFA[team_name]

    def _get_standings_sorted_opponents(self, ranking_fifa, team_matches, team_name):
        finished_matches = [match for match in team_matches if match.get(ConfigConstants.STATUS) == ConfigLoader().get_selector(ConfigConstants.STATUS_MATCH_FINISHED_SELECTOR)]
        standings_opponents = {}
        for finished_match in finished_matches:
            opponent = finished_match[ConfigConstants.OPPONENT]
            self._update_ranking_fifa(opponent, ranking_fifa)
            if opponent in ranking_fifa:
                standings_opponents[opponent] = {
                    ConfigConstants.POSITION: ranking_fifa[opponent],
                    ConfigConstants.RESULT_TENDENCY: self._get_all_results_tendencies(opponent, finished_match[ConfigConstants.RESULT], team_name)
                }
        return dict(sorted(standings_opponents.items(), key=lambda item: item[1][ConfigConstants.POSITION]))

    def _get_all_results_tendencies(self, opponent, result_data, team_name):
        result_tendency = self._get_result_tendency(result_data[ConfigConstants.FULL_TIME][team_name], result_data[ConfigConstants.FULL_TIME][opponent])
        result_tendency += self._get_result_tendency(result_data[ConfigConstants.FIRST_HALF][team_name], result_data[ConfigConstants.FIRST_HALF][opponent])
        result_tendency += self._get_result_tendency(result_data[ConfigConstants.SECOND_HALF][team_name], result_data[ConfigConstants.SECOND_HALF][opponent])
        if result_data[ConfigConstants.HAS_EXTRA_TIME]:
            result_tendency += self._get_result_tendency(result_data[ConfigConstants.EXTRA_TIME][team_name], result_data[ConfigConstants.EXTRA_TIME][opponent])
        if result_data[ConfigConstants.HAS_PENALTIES]:
            result_tendency += self._get_result_tendency(result_data[ConfigConstants.PENALTIES][team_name], result_data[ConfigConstants.PENALTIES][opponent])
        return result_tendency

    @staticmethod
    def _get_result_tendency(team_name_goals, opponent_goals):
        result_tendency = ConfigConstants.RESULT_TENDENCY_DRAW
        if team_name_goals > opponent_goals:
            result_tendency = ConfigConstants.RESULT_TENDENCY_WIN
        elif team_name_goals < opponent_goals:
            result_tendency = ConfigConstants.RESULT_TENDENCY_LOST
        return [team_name_goals, opponent_goals, result_tendency]
