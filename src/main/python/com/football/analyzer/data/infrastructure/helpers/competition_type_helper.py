import logging

from ...commons.config.config_constants import ConfigConstants
from ...commons.config.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class CompetitionTypeHelper:

    def __init__(self,):
        self._config_loader = ConfigLoader()
        self._competitions_types_config = self._config_loader.get_competitions_types_config()

    def get_competition_type(self, federation_name: str, competition_name: str):
        competition_type = None
        if ConfigConstants.FIFA == federation_name and ConfigConstants.WORLD_CUP == competition_name:
            competition_type = f'{ConfigConstants.FIFA}_{ConfigConstants.WORLD_CUP}'
        else:
            for competition_type_config in self._competitions_types_config:
                if f'{federation_name}-{competition_name}' in competition_type_config[ConfigConstants.COMPETITIONS].split(','):
                    competition_type = competition_type_config.name
                    break
        return competition_type
