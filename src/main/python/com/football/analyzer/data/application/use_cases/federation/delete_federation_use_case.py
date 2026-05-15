from dataclasses import dataclass

from ....application.dto.federation_request_dto import DeleteFederationRequestDTO
from ....domain.ports.repositories.federation_repository_port import FederationRepositoryPort


@dataclass
class DeleteFederationResult:
    success: bool
    message: str


class DeleteFederationUseCase:

    def __init__(self, federation_repository: FederationRepositoryPort):
        self._federation_repository = federation_repository

    def execute(self, dto: DeleteFederationRequestDTO) -> DeleteFederationResult:
        validation_error = dto.validate()
        if validation_error:
            return DeleteFederationResult(
                success=False,
                message=validation_error
            )
        try:
            exists = self._federation_repository.federation_exists(dto.federation_name)
            if not exists:
                return DeleteFederationResult(
                    success=False,
                    message=f"Federation '{dto.federation_name}' not found"
                )
            collection = self._federation_repository.get_collection()
            result = collection.delete_one({'name': dto.federation_name})
            if result.deleted_count > 0:
                return DeleteFederationResult(
                    success=True,
                    message=f"Federation '{dto.federation_name}' deleted"
                )
            else:
                return DeleteFederationResult(
                    success=False,
                    message=f"Failed to delete federation '{dto.federation_name}'"
                )
        except Exception as e:
            return DeleteFederationResult(
                success=False,
                message=f"Error: {str(e)}"
            )
