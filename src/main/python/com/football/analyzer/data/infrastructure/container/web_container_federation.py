from ..adapters.repositories.mongodb_federation_repository import MongoDBFederationRepository
from ...application.use_cases.federation.create_or_update_federation_from_web_use_case import CreateOrUpdateFederationFromWebUseCase
from ...application.use_cases.federation.delete_federation_use_case import DeleteFederationUseCase
from ...application.use_cases.federation.get_all_federations_use_case import GetAllFederationsUseCase
from ...application.use_cases.calendar.get_calendars_use_case import GetCalendarsUseCase
from ...application.use_cases.federation.get_federations_use_case import GetFederationsUseCase
from ...application.use_cases.calendar.get_upcoming_matches_of_calendars_use_case import GetUpcomingMatchesUseCase
from ...domain.ports.repositories.database_connection_port import DatabaseConnectionPort
from ...domain.ports.repositories.federation_repository_port import FederationRepositoryPort
from .notification_container import NotificationContainer


class WebContainerFederation:

    def __init__(
        self,
        db_connection: DatabaseConnectionPort,
        notification_container: NotificationContainer,
        app=None
    ):
        self._db_connection = db_connection
        self._app = app
        self._notification_container = notification_container
        self._federation_repository = None

    @property
    def app(self):
        return self._app

    @property
    def federation_repository(self) -> FederationRepositoryPort:
        if self._federation_repository is None:
            self._federation_repository = MongoDBFederationRepository(self._db_connection)
        return self._federation_repository

    @property
    def create_or_update_from_web_use_case(self) -> CreateOrUpdateFederationFromWebUseCase:
        return CreateOrUpdateFederationFromWebUseCase(
            self.federation_repository,
            self._notification_container.notification_service,
            self._app
        )

    @property
    def get_federations_use_case(self) -> GetFederationsUseCase:
        return GetFederationsUseCase(self.federation_repository)

    @property
    def get_all_federations_use_case(self) -> GetAllFederationsUseCase:
        return GetAllFederationsUseCase(self.federation_repository)

    @property
    def get_calendars_use_case(self) -> GetCalendarsUseCase:
        return GetCalendarsUseCase(self.federation_repository)

    @property
    def get_upcoming_matches_use_case(self) -> GetUpcomingMatchesUseCase:
        return GetUpcomingMatchesUseCase(self.get_calendars_use_case)

    @property
    def delete_federation_use_case(self) -> DeleteFederationUseCase:
        return DeleteFederationUseCase(self.federation_repository)
