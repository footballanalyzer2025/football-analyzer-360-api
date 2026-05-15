import logging
from dataclasses import dataclass
from typing import Dict, Any

from ....application.dto.team_request_dto import GetTeamsRequestDTO
from ....commons.config.config_constants import ConfigConstants
from ....domain.ports.repositories.team_repository_port import TeamRepositoryPort

logger = logging.getLogger(__name__)


@dataclass
class GetTeamsResult:
    success: bool
    message: str
    data: Dict[str, Dict[str, Any]]


class GetTeamsUseCase:

    def __init__(self, team_repository: TeamRepositoryPort):
        self._team_repository = team_repository

    def execute(self, dto: GetTeamsRequestDTO) -> GetTeamsResult:
        validation_error = dto.validate()
        if validation_error:
            return GetTeamsResult(
                success=False,
                message=validation_error,
                data={}
            )
        try:
            collection = self._team_repository.get_collection()
            cursor = collection.find(
                {ConfigConstants.NAME: {'$in': dto.teams_data}},
                {'_id': 0}
            )
            result_data = {}
            for doc in cursor:
                result_data[doc[ConfigConstants.NAME]] = {k: v for k, v in doc.items() if k != ConfigConstants.NAME}
            return GetTeamsResult(
                success=True,
                message=f"Found {len(result_data)} teams",
                data=result_data
            )
        except Exception as e:
            logger.error(f"Error getting teams: {e}")
            return GetTeamsResult(
                success=False,
                message=f"Error: {str(e)}",
                data={}
            )
