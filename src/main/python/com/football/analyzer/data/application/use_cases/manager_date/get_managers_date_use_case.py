import logging
from dataclasses import dataclass
from typing import Dict

from ....application.dto.manager_date_request_dto import GetManagersDateRequestDTO
from ....commons.config.config_constants import ConfigConstants
from ....domain.ports.repositories.manager_date_repository_port import ManagerDateRepositoryPort

logger = logging.getLogger(__name__)


@dataclass
class GetManagersDateResult:
    success: bool
    message: str
    data: Dict[str, str]


class GetManagersDateUseCase:

    def __init__(self, manager_repository: ManagerDateRepositoryPort):
        self._manager_repository = manager_repository

    def execute(self, dto: GetManagersDateRequestDTO) -> GetManagersDateResult:
        validation_error = dto.validate()
        if validation_error:
            return GetManagersDateResult(
                success=False,
                message=validation_error,
                data={}
            )

        try:
            collection = self._manager_repository.get_collection()
            cursor = collection.find(
                {ConfigConstants.TEAM_NAME: {'$in': dto.team_managers}},
                {'_id': 0, ConfigConstants.TEAM_NAME: 1, ConfigConstants.MANAGER_START_DATE: 1}
            )

            result_data = {}
            for doc in cursor:
                result_data[doc[ConfigConstants.TEAM_NAME]] = doc.get(ConfigConstants.MANAGER_START_DATE, '')

            return GetManagersDateResult(
                success=True,
                message=f"Found {len(result_data)} managers",
                data=result_data
            )

        except Exception as e:
            logger.error(f"Error getting managers: {e}")
            return GetManagersDateResult(
                success=False,
                message=f"Error: {str(e)}",
                data={}
            )
