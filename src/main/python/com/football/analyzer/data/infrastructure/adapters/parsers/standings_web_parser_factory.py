from main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from main.python.com.football.analyzer.data.domain.ports.standings.standings_web_parser_port import StandingsWebParserPort
from main.python.com.football.analyzer.data.infrastructure.adapters.standings.fifa_world_cup_web_standings_parser_adapter import FifaWorldCupStandingsWebParserAdapter


class StandingsWebParserFactory:
    _parsers = {
        f'{ConfigConstants.FIFA}_{ConfigConstants.WORLD_CUP}': FifaWorldCupStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_LIGA_STANDARD: LigaStandardStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_LIGA_ARGENTINA: LigaArgentinaStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_LIGA_COLOMBIA: LigaColombiaStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_NATIONAL_TEAM_CUP: NationalTeamCupStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_CONTINENTAL_CLUB_CUP: ContinentalTeamCupStandingsWebParserAdapter()
        # ConfigConstants.LF_COMPETITION_TYPE_CONTINENTAL_LIGA_CUP: ContinentalLigaCupStandingsWebParserAdapter()
    }

    @classmethod
    def get_parser(cls, competition_type: str) -> StandingsWebParserPort:
        return cls._parsers[competition_type]
