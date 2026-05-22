from main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from main.python.com.football.analyzer.data.domain.ports.standings.standings_web_parser_port import StandingsWebParserPort
from main.python.com.football.analyzer.data.infrastructure.adapters.standings.fifa_world_cup_web_standings_parser_adapter import FifaWorldCupStandingsWebParserAdapter


class StandingsWebParserFactory:
    _parsers = {
        f'{ConfigConstants.FIFA}-{ConfigConstants.WORLD_CUP}': FifaWorldCupStandingsWebParserAdapter()
    }

    @classmethod
    def get_parser(cls, competition_type: str) -> StandingsWebParserPort:
        return cls._parsers[competition_type]
