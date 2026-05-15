from src.main.python.com.football.analyzer.data.application.dto.manager_date_response_dto import GetAllManagerDatesResponseDTO
from src.main.python.com.football.analyzer.data.domain.ports.repositories.manager_date_repository_port import ManagerDateRepositoryPort


class GetAllManagerDatesUseCase:

    def __init__(self, repository: ManagerDateRepositoryPort):
        self._repository = repository

    def execute(self) -> GetAllManagerDatesResponseDTO:
        managers = self._repository.get_all()
        return GetAllManagerDatesResponseDTO(
            managers=managers,
            count=len(managers),
            success=True
        )
