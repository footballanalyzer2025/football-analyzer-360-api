from typing import Dict, List

from main.python.com.football.analyzer.data.domain.ports.standings.match_standings_stats_port import MatchStandingsStatsPort


class MatchStandingsStatsAdapter(MatchStandingsStatsPort):

    def get_match_standings_stats(self, standing: Dict, team_matches: List, opponent: str) -> Dict:
        pass
