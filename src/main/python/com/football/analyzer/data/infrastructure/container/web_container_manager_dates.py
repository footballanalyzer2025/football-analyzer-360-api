from ..adapters.repositories.mongodb_manager_date_repository import MongoDBManagerDateRepository
from ...application.use_cases.manager_date.create_or_update_manager_date_use_case import CreateOrUpdateManagerDateUseCase
from ...application.use_cases.manager_date.delete_manager_date_use_case import DeleteManagerDateUseCase
from ...application.use_cases.manager_date.get_all_manager_dates_use_case import GetAllManagerDatesUseCase
from ...application.use_cases.manager_date.get_managers_date_use_case import GetManagersDateUseCase
from ...domain.ports.repositories.database_connection_port import DatabaseConnectionPort
from ...domain.ports.repositories.manager_date_repository_port import ManagerDateRepositoryPort


class WebContainerManagerDates:

    def __init__(self, db_connection: DatabaseConnectionPort):
        self._db_connection = db_connection
        self._manager_repository = None

    @property
    def manager_repository(self) -> ManagerDateRepositoryPort:
        if self._manager_repository is None:
            self._manager_repository = MongoDBManagerDateRepository(self._db_connection)
        return self._manager_repository

    @property
    def create_or_update_use_case(self) -> CreateOrUpdateManagerDateUseCase:
        return CreateOrUpdateManagerDateUseCase(self.manager_repository)

    @property
    def get_managers_use_case(self) -> GetManagersDateUseCase:
        return GetManagersDateUseCase(self.manager_repository)

    @property
    def get_all_managers_use_case(self) -> GetAllManagerDatesUseCase:
        return GetAllManagerDatesUseCase(self.manager_repository)

    @property
    def delete_manager_use_case(self) -> DeleteManagerDateUseCase:
        return DeleteManagerDateUseCase(self.manager_repository)
