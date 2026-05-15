from src.main.python.com.football.analyzer.data.application.dto.manager_date_request_dto import DeleteManagerDateRequestDTO
from src.main.python.com.football.analyzer.data.application.dto.manager_date_response_dto import OperationResultDTO
from src.main.python.com.football.analyzer.data.domain.ports.repositories.manager_date_repository_port import ManagerDateRepositoryPort


class DeleteManagerDateUseCase:

    def __init__(self, repository: ManagerDateRepositoryPort):
        self._repository = repository

    def execute(self, request: DeleteManagerDateRequestDTO) -> OperationResultDTO:
        if not self._repository.exists(request.team_name):
            return OperationResultDTO(
                success=False,
                message=f"Team '{request.team_name}' not found"
            )
        deleted = self._repository.delete(request.team_name)
        if deleted:
            return OperationResultDTO(
                success=True,
                message=f"Team '{request.team_name}' deleted successfully"
            )
        return OperationResultDTO(
            success=False,
            message=f"Failed to delete team '{request.team_name}'"
        )
