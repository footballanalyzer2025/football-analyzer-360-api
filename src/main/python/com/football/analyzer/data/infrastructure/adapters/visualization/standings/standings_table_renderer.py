import re
import matplotlib.pyplot as plt
import pandas as pd

from datetime import datetime
from matplotlib.patches import Rectangle

import matplotlib
matplotlib.use('Agg')


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

    def create_combined_figure(self,
                               df_home: pd.DataFrame,
                               df_away: pd.DataFrame,
                               home_team_name: str,
                               away_team_name: str) -> plt.Figure:
        max_rows = max(len(df_home), len(df_away))
        fig_height = max(9, int((max_rows + 1) * 0.65))
        fig, axes = plt.subplots(2, 2, figsize=(16, fig_height))
        fig.suptitle(f"{home_team_name} vs {away_team_name} - Standings Comparison", fontsize=14, fontweight='bold')
        df_away_inverted = self._invert_away_match_results(df_away)
        self._draw_team_tables(axes[0, 0], axes[0, 1], df_home, home_team_name)
        self._draw_team_tables(axes[1, 0], axes[1, 1], df_away_inverted, away_team_name)
        plt.subplots_adjust(top=0.92, bottom=0.05, hspace=0.4, wspace=0.3)
        return fig

    @staticmethod
    def _invert_away_match_results(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        def invert(match_data):
            if isinstance(match_data, list):
                inverted = []
                for i in range(0, len(match_data), 3):
                    if i + 2 < len(match_data):
                        g1, g2, res = match_data[i], match_data[i + 1], match_data[i + 2]
                        inverted.extend([g2, g1, res])
                    else:
                        inverted.extend(match_data[i:])
                return inverted
            else:
                return match_data
        df['Match'] = df['Match'].apply(invert)
        return df

    def _draw_team_tables(self, ax_pos, ax_date, df: pd.DataFrame, team_label: str):
        if df.empty:
            for ax in [ax_pos, ax_date]:
                ax.text(0.5, 0.5, 'No data', ha='center', va='center', fontsize=10)
                ax.axis('off')
            return
        df_pos = df.sort_values('Position').reset_index(drop=True)
        df_date = self._sort_by_date(df)
        self._draw_table(ax_pos, df_pos, title=f"{team_label} - Sorted by Position")
        self._draw_table(ax_date, df_date, title=f"{team_label} - Sorted by Date")

    def _draw_table(self, ax, df: pd.DataFrame, title: str):
        ax.axis('off')
        if 'Match' in df.columns:
            expanded_df = self._expand_match_column(df)
        else:
            expanded_df = df
        cols = list(expanded_df.columns)
        period_names = ['1st', '2nd', 'FT', 'ET', 'PK']
        title_row = [title] + [''] * (len(cols) - 1)
        header_row = list(cols)
        data_rows = [list(row) for _, row in expanded_df.iterrows()]
        cell_text = [title_row, header_row] + data_rows
        table = ax.table(cellText=cell_text, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(6)
        table.scale(1.0, 1.2)
        for (row, col), cell in table.get_celld().items():
            col_name = cols[col] if col < len(cols) else ''
            if col_name == 'Position':
                cell.set_width(0.08)
            elif col_name == 'Opponent':
                cell.set_width(0.22)
            elif col_name == 'Date':
                cell.set_width(0.12)
            else:
                cell.set_width(0.1)
            if row == 0:
                cell.set_height(0.04)
                cell.set_facecolor('#006064')
                cell.set_text_props(color='white', fontweight='bold')
                central_col = len(cols) // 2
                if col == central_col:
                    cell.get_text().set_text(title)
                else:
                    cell.get_text().set_text('')
            elif row == 1:
                cell.set_facecolor('#006064')
                cell.set_text_props(color='white', fontweight='bold')
            else:
                if col_name in period_names:
                    text = cell.get_text().get_text()
                    result_letter = self._extract_result_letter(text)
                    if result_letter == 'W':
                        cell.set_facecolor('#2E7D32')
                    elif result_letter == 'D':
                        cell.set_facecolor('#D4AF37')
                    elif result_letter == 'L':
                        cell.set_facecolor('#D32F2F')
                    else:
                        cell.set_facecolor('white')
                    cell.set_text_props(color='white')
                else:
                    cell.set_facecolor('white')
                    cell.set_text_props(color='black')

    @staticmethod
    def _expand_match_column(df: pd.DataFrame) -> pd.DataFrame:
        period_names = ['1st', '2nd', 'FT', 'ET', 'PK']
        rows = []
        for _, row in df.iterrows():
            pos = row['Position']
            opp = row['Opponent']
            date = row['Date']
            match_data = row['Match']
            if isinstance(match_data, list):
                period_values = {}
                for i, name in enumerate(period_names):
                    start = i * 3
                    if start + 2 < len(match_data):
                        g1, g2, res = match_data[start], match_data[start + 1], match_data[start + 2]
                        period_values[name] = f"{g1}-{g2} ({res})"
                    else:
                        period_values[name] = ""
            else:
                period_values = {name: "" for name in period_names}
            rows.append({
                'Position': pos,
                'Opponent': opp,
                'Date': date,
                **period_values
            })
        expanded = pd.DataFrame(rows)
        col_order = ['Position', 'Opponent'] + period_names + ['Date']
        return expanded[col_order]

    @staticmethod
    def _extract_result_letter(text: str) -> str:
        m = re.search(r'\((\w)\)', text)
        return m.group(1) if m else ''
