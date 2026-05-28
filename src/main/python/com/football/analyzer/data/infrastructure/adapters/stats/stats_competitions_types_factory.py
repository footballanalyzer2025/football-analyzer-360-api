from main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from main.python.com.football.analyzer.data.domain.ports.stats.analysis_stats_strategy import AnalysisStatsStrategy
from main.python.com.football.analyzer.data.infrastructure.adapters.stats.fifa_world_cup_analysis_stats_strategy import FifaWorldCupAnalysisStatsStrategy


class StatsCompetitionsTypesFactory:

    _parsers = {
        f'{ConfigConstants.FIFA}_{ConfigConstants.WORLD_CUP}': FifaWorldCupAnalysisStatsStrategy()
        # ConfigConstants.LF_COMPETITION_TYPE_LIGA_STANDARD: LigaStandardStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_LIGA_ARGENTINA: LigaArgentinaStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_LIGA_COLOMBIA: LigaColombiaStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_NATIONAL_TEAM_CUP: NationalTeamCupStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_CONTINENTAL_CLUB_CUP: ContinentalTeamCupStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_CONTINENTAL_LIGA_CUP: ContinentalLigaCupStandingsWebParserAdapter()
    }

    @classmethod
    def get_stats(cls, competition_type: str) -> AnalysisStatsStrategy:
        return cls._parsers[competition_type]
