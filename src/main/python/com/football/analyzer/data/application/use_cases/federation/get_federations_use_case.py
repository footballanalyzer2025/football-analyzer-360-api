import logging
from dataclasses import dataclass
from typing import Dict, Any, List

from ....application.dto.federation_request_dto import GetFederationsRequestDTO
from ....commons.config.config_constants import ConfigConstants
from ....domain.ports.repositories.federation_repository_port import FederationRepositoryPort

logger = logging.getLogger(__name__)


@dataclass
class GetFederationsResult:
    success: bool
    message: str
    count: int
    federations: List[Dict[str, Any]]


class GetFederationsUseCase:

    def __init__(self, federation_repository: FederationRepositoryPort):
        self._federation_repository = federation_repository

    def execute(self, dto: GetFederationsRequestDTO) -> GetFederationsResult:
        validation_error = dto.validate()
        if validation_error:
            return GetFederationsResult(
                success=False,
                message=validation_error,
                count=0,
                federations=[]
            )

        try:
            collection = self._federation_repository.get_collection()
            requested_federations = list(dto.competitions_by_federation.keys())

            cursor = collection.find(
                {ConfigConstants.NAME: {'$in': requested_federations}},
                {'_id': 0}
            )
            federations = list(cursor)

            return GetFederationsResult(
                success=True,
                message=f"Found {len(federations)} federations",
                count=len(federations),
                federations=federations
            )

        except Exception as e:
            logger.error(f"Error getting federations: {e}")
            return GetFederationsResult(
                success=False,
                message=f"Error: {str(e)}",
                count=0,
                federations=[]
            )
