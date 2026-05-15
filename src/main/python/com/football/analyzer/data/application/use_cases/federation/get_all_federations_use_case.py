from dataclasses import dataclass
from typing import List, Dict, Any

from ....domain.ports.repositories.federation_repository_port import FederationRepositoryPort


@dataclass
class GetAllFederationsResult:
    success: bool
    count: int
    federations: List[Dict[str, Any]]


class GetAllFederationsUseCase:

    def __init__(self, federation_repository: FederationRepositoryPort):
        self._federation_repository = federation_repository

    def execute(self) -> GetAllFederationsResult:
        federations = list(self._federation_repository.get_collection().find({}, {'_id': 0}))
        return GetAllFederationsResult(
            success=True,
            count=len(federations),
            federations=federations
        )
