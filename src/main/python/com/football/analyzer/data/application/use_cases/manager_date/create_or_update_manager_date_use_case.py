from src.main.python.com.football.analyzer.data.application.dto.manager_date_request_dto import CreateOrUpdateManagerDateRequestDTO
from src.main.python.com.football.analyzer.data.application.dto.manager_date_response_dto import OperationResultDTO
from src.main.python.com.football.analyzer.data.domain.ports.repositories.manager_date_repository_port import ManagerDateRepositoryPort


class CreateOrUpdateManagerDateUseCase:

    def __init__(self, repository: ManagerDateRepositoryPort):
        self._repository = repository

    def execute(self, request: CreateOrUpdateManagerDateRequestDTO) -> OperationResultDTO:
        results = self._repository.save_many(request.managers_data)
        failed = [name for name, success in results.items() if not success]
        if failed:
            return OperationResultDTO(
                success=False,
                message=f"Failed to save {len(failed)} teams: {', '.join(failed[:5])}",
                data=results
            )
        return OperationResultDTO(
            success=True,
            message=f"Successfully saved {len(results)} teams",
            data=results
        )
