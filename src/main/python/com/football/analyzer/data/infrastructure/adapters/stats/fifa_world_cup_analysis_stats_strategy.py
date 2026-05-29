from typing import Dict, Any

from matplotlib import pyplot as plt

from main.python.com.football.analyzer.data.application.services.standings.standings_table_builder import StandingsTableBuilder
from main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from main.python.com.football.analyzer.data.domain.ports.stats.analysis_stats_strategy import AnalysisStatsStrategy
from main.python.com.football.analyzer.data.infrastructure.adapters.standings.fifa_world_ranking_excel_adapter import FifaWorldRankingExcelAdapter
from main.python.com.football.analyzer.data.infrastructure.adapters.visualization.standings.standings_table_renderer import StandingsTableRenderer


class FifaWorldCupAnalysisStatsStrategy(AnalysisStatsStrategy):

    def execute(self, path_to_save_analysis: str, match_to_analyze: Dict[str, Any], all_teams: Dict[str, Dict[str, Any]], all_standings_competition: Dict):
        home_team_data_to_analyze, away_team_data_to_analyze = self._get_teams_data_to_analyze(all_standings_competition, all_teams, match_to_analyze)
        home_opponents_standings, away_opponents_standings = self._get_opponents_standings_to_teams(away_team_data_to_analyze, home_team_data_to_analyze, match_to_analyze)
        self._get_figs_of_teams(path_to_save_analysis, home_opponents_standings, away_opponents_standings, match_to_analyze)
        return None

    def _get_teams_data_to_analyze(self, all_standings_competition, all_teams, match_to_analyze):
        all_standings_competition[ConfigConstants.GENERAL_STANDING] = FifaWorldRankingExcelAdapter(ConfigLoader().get_fifa_world_ranking_file_special_case()).load_ranking()
        return (self._get_team_data_to_analyze(ConfigConstants.HOME_TEAM, all_standings_competition, all_teams, match_to_analyze),
                self._get_team_data_to_analyze(ConfigConstants.AWAY_TEAM, all_standings_competition, all_teams, match_to_analyze))

    def _get_team_data_to_analyze(self, venue_team, all_standings_competition, all_teams, match_to_analyze) -> Dict:
        team_name = match_to_analyze[venue_team]
        ranking_fifa = all_standings_competition[ConfigConstants.GENERAL_STANDING]
        team_matches = all_teams[match_to_analyze[venue_team]][ConfigConstants.MATCHES][ConfigConstants.ALL_MATCHES]
        return {
            team_name: {
                ConfigConstants.POSITION: ranking_fifa[team_name],
                ConfigConstants.OPPONENTS_DATA: self._get_standings_sorted_opponents(ranking_fifa, team_matches, team_name)
            }
        }

    def _get_standings_sorted_opponents(self, ranking_fifa, team_matches, team_name):
        finished_matches = [match for match in team_matches if match.get(ConfigConstants.STATUS) == ConfigLoader().get_selector(ConfigConstants.STATUS_MATCH_FINISHED_SELECTOR)]
        standings_opponents = {}
        for finished_match in finished_matches:
            opponent = finished_match[ConfigConstants.OPPONENT]
            if opponent in ranking_fifa:
                standings_opponents[opponent] = {
                    ConfigConstants.POSITION: ranking_fifa[opponent],
                    ConfigConstants.RESULT_TENDENCY: self._get_all_results_tendencies(opponent, finished_match[ConfigConstants.RESULT], team_name),
                    ConfigConstants.DATE: finished_match[ConfigConstants.DATE]
                }
        return dict(sorted(standings_opponents.items(), key=lambda item: item[1][ConfigConstants.POSITION]))

    def _get_all_results_tendencies(self, opponent, result_data, team_name):
        result_tendency = self._get_result_tendency(result_data[ConfigConstants.FIRST_HALF][team_name], result_data[ConfigConstants.FIRST_HALF][opponent])
        result_tendency += self._get_result_tendency(result_data[ConfigConstants.SECOND_HALF][team_name], result_data[ConfigConstants.SECOND_HALF][opponent])
        result_tendency += self._get_result_tendency(result_data[ConfigConstants.FULL_TIME][team_name], result_data[ConfigConstants.FULL_TIME][opponent])
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

    def _get_opponents_standings_to_teams(self, away_team_data_to_analyze, home_team_data_to_analyze, match_to_analyze):
        builder = StandingsTableBuilder()
        away_team_name = match_to_analyze[ConfigConstants.AWAY_TEAM]
        home_team_name = match_to_analyze[ConfigConstants.HOME_TEAM]
        return (self._get_opponent_standings_played_to_team(builder, home_team_data_to_analyze, away_team_data_to_analyze[away_team_name][ConfigConstants.POSITION], away_team_name),
                self._get_opponent_standings_played_to_team(builder, away_team_data_to_analyze, home_team_data_to_analyze[home_team_name][ConfigConstants.POSITION], home_team_name))

    @staticmethod
    def _get_opponent_standings_played_to_team(builder, team_data_to_analyze, opponent_position, opponent_team_name):
        return builder.build_from_team_data(
            team_data=team_data_to_analyze,
            opponent_name=opponent_team_name,
            opponent_position=opponent_position
        )

    @staticmethod
    def _get_figs_of_teams(path_to_save_analysis, home_opponents_standings, away_opponents_standings, match_to_analyze):
        renderer = StandingsTableRenderer()
        home_team_name = match_to_analyze[ConfigConstants.HOME_TEAM]
        away_team_name = match_to_analyze[ConfigConstants.AWAY_TEAM]
        fig_home = renderer.create_figure(home_opponents_standings, home_team_name, away_team_name)
        fig_home.savefig(f"{path_to_save_analysis}\\{home_team_name} Vs {away_team_name}.png", dpi=150)
        plt.close(fig_home)
        fig_away = renderer.create_figure(away_opponents_standings, away_team_name, home_team_name)
        fig_away.savefig(f"{path_to_save_analysis}\\{away_team_name} Vs {home_team_name}.png", dpi=150)
        plt.close(fig_away)
