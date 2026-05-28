import os
import pandas as pd
from typing import Dict


class FifaWorldRankingExcelAdapter:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_ranking(self) -> Dict[str, int]:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Ranking File Not Found: {self.file_path}")
        homologation_df = pd.read_excel(self.file_path, sheet_name='Homologation')
        ranking_df = pd.read_excel(self.file_path, sheet_name='Ranking')
        ranking_dict = dict(zip(ranking_df['FIFA Team Name'], ranking_df['Position']))
        livefutbol_ranking = {}
        for _, row in homologation_df.iterrows():
            livefutbol_name = row['LiveFutbol Team Name']
            fifa_name = row['FIFA Team Name']
            if fifa_name in ranking_dict:
                livefutbol_ranking[livefutbol_name] = ranking_dict[fifa_name]
        return livefutbol_ranking
