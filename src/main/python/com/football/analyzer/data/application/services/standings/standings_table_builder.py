from typing import Dict, List, Optional, Any
import pandas as pd

from main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants


class StandingsTableBuilder:

    def __init__(self):
        self._rows: List[Dict[str, Any]] = []

    def build_from_team_data(
        self,
        team_data: Dict[str, Any],
        opponent_name: Optional[str] = None,
        opponent_position: Optional[int] = None
    ) -> pd.DataFrame:
        self._rows = []
        team_name = next(iter(team_data))
        team_info = team_data[team_name]
        opponents_data = team_info[ConfigConstants.OPPONENTS_DATA]
        for opponent, op_data in opponents_data.items():
            self._add_row(
                position=op_data[ConfigConstants.POSITION],
                opponent=opponent,
                result_tendency=op_data[ConfigConstants.RESULT_TENDENCY],
                date=op_data[ConfigConstants.DATE],
                is_next_opponent=False
            )
        if opponent_name and opponent_name not in opponents_data:
            self._add_row(
                position=opponent_position,
                opponent=opponent_name,
                result_tendency=None,
                date=None,
                is_next_opponent=True
            )
        return self._to_dataframe()

    def _add_row(self, position: int, opponent: str, result_tendency: Optional[List], date: Optional[str], is_next_opponent: bool):
        self._rows.append({
            'Position': position,
            'Opponent': opponent,
            'Match': result_tendency if result_tendency else 'To Analyze',
            'Date': date if date else 'Next Game',
            'IsNextOpponent': is_next_opponent
        })

    def _to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self._rows)
        if not df.empty:
            df = df.sort_values('Position').reset_index(drop=True)
        return df
