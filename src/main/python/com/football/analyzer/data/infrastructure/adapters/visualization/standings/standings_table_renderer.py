import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


class StandingsTableRenderer:

    def create_figure(self, df: pd.DataFrame, team_name: str, opponent_team_name: str) -> plt.Figure:
        if df.empty:
            fig, ax = plt.subplots(figsize=(10, 2))
            ax.text(0.5, 0.5, 'Data not available', ha='center', va='center', fontsize=12)
            ax.axis('off')
            return fig
        fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(16, max(6, int(len(df) * 0.4))))
        fig.suptitle(f"{team_name} - History Vs. Opponents (Next Opponent: {opponent_team_name})", fontsize=14, fontweight='bold')
        df_pos = df.sort_values('Position').reset_index(drop=True)
        self._draw_table(ax_left, df_pos, title="Sort By Position")
        df_date = self._sort_by_date(df)
        self._draw_table(ax_right, df_date, title="Sort By Date")
        plt.tight_layout()
        return fig

    @staticmethod
    def _sort_by_date(df: pd.DataFrame) -> pd.DataFrame:
        def parse_date(val):
            if val == 'Next Game' or pd.isna(val) or val is None:
                return pd.NaT
            try:
                return datetime.strptime(val, '%d.%m.%Y')
            except (ValueError, TypeError):
                return pd.NaT

        df_copy = df.copy()
        df_copy['_date_parsed'] = df_copy['Date'].apply(parse_date)
        df_sorted = df_copy.sort_values('_date_parsed', ascending=False, na_position='last')
        df_sorted = df_sorted.drop(columns=['_date_parsed']).reset_index(drop=True)
        return df_sorted

    def _draw_table(self, ax, df: pd.DataFrame, title: str):
        ax.axis('tight')
        ax.axis('off')
        ax.set_title(title, fontsize=12, fontweight='bold')
        display_df = df[['Position', 'Opponent', 'Match', 'Date']].copy()
        display_df['Match'] = display_df['Match'].apply(
            lambda x: self._format_result_tendency(x) if isinstance(x, list) else str(x)
        )
        table = ax.table(
            cellText=display_df.values,
            colLabels=display_df.columns,
            cellLoc='center',
            loc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.0, 1.2)
        for (row, col), cell in table.get_celld().items():
            if col == 0:
                cell.set_width(0.12)
            elif col == 1:
                cell.set_width(0.3)
            elif col == 2:
                cell.set_width(0.4)
            elif col == 3:
                cell.set_width(0.18)

    @staticmethod
    def _format_result_tendency(tendency: list) -> str:
        if not tendency:
            return "To Analyze"
        parts = []
        for i in range(0, len(tendency), 3):
            if i+2 < len(tendency):
                parts.append(f"{tendency[i]}-{tendency[i+1]} ({tendency[i+2]})")
        return " | ".join(parts)
