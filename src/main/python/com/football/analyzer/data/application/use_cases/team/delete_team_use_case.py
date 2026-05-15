import logging
from dataclasses import dataclass

from ....application.dto.team_request_dto import DeleteTeamRequestDTO
from ....commons.config.config_constants import ConfigConstants
from ....domain.ports.repositories.team_repository_port import TeamRepositoryPort

logger = logging.getLogger(__name__)


@dataclass
class DeleteTeamResult:
    success: bool
    message: str


class DeleteTeamUseCase:

    def __init__(self, team_repository: TeamRepositoryPort):
        self._team_repository = team_repository
        self.fields_list = [
            ConfigConstants.HAS_MANAGER_DATA,
            ConfigConstants.MANAGER_START_DATE,
            ConfigConstants.SECTIONS,
            ConfigConstants.MATCHES,
            ConfigConstants.CREATED_AT,
            ConfigConstants.UPDATE_AT
        ]

    def execute(self, dto: DeleteTeamRequestDTO) -> DeleteTeamResult:
        validation_error = dto.validate()
        if validation_error:
            return DeleteTeamResult(
                success=False,
                message=validation_error
            )
        team_to_delete = dto.team_to_delete
        try:
            collection = self._team_repository.get_collection()
            existing = collection.find_one({ConfigConstants.NAME: team_to_delete})
            if not existing:
                return DeleteTeamResult(
                    success=False,
                    message=f"Team '{team_to_delete}' not found"
                )
            for field in self.fields_list:
                result = collection.update_one(
                    {ConfigConstants.NAME: team_to_delete},
                    {'$unset': {field: ""}}
                )
            logger.info(f"Team '{team_to_delete}' soft deleted successfully")
            return DeleteTeamResult(
                success=True,
                message=f"Team '{team_to_delete}' soft deleted"
            )
        except Exception as e:
            logger.error(f"Error soft deleting team '{team_to_delete}': {e}")
            return DeleteTeamResult(
                success=False,
                message=f"Error: {str(e)}"
            )
