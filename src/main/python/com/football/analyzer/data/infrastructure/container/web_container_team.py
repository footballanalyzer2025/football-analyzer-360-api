from .notification_container import NotificationContainer
from .web_container_federation import WebContainerFederation
from .web_container_manager_dates import WebContainerManagerDates
from ..adapters.repositories.mongodb_team_repository import MongoDBTeamRepository
from ...application.use_cases.team.create_teams_from_list_use_case import CreateTeamsFromListUseCase
from ...application.use_cases.team.create_teams_from_web_use_case import CreateTeamsFromWebUseCase
from ...application.use_cases.team.delete_team_use_case import DeleteTeamUseCase
from ...application.use_cases.team.get_all_teams_use_case import GetAllTeamsUseCase
from ...application.use_cases.team.get_teams_use_case import GetTeamsUseCase
from ...domain.ports.repositories.database_connection_port import DatabaseConnectionPort
from ...domain.ports.repositories.team_repository_port import TeamRepositoryPort


class WebContainerTeam:
    def __init__(
        self,
        db_connection: DatabaseConnectionPort,
        web_container_manager_dates: WebContainerManagerDates,
        web_container_federation: WebContainerFederation,
        notification_container: NotificationContainer,
        app=None
    ):
        self._db_connection = db_connection
        self._team_repository = None
        self._web_container_manager_dates = web_container_manager_dates
        self._web_container_federation = web_container_federation
        self._notification_container = notification_container
        self._app = app

    @property
    def app(self):
        return self._app

    @property
    def team_repository(self) -> TeamRepositoryPort:
        if self._team_repository is None:
            self._team_repository = MongoDBTeamRepository(self._db_connection)
        return self._team_repository

    @property
    def create_teams_from_web_use_case(self) -> CreateTeamsFromWebUseCase:
        return CreateTeamsFromWebUseCase(self._web_container_manager_dates,
                                         self._web_container_federation,
                                         self.team_repository,
                                         self._notification_container.notification_service,
                                         self._app)

    @property
    def create_teams_from_list_use_case(self) -> CreateTeamsFromListUseCase:
        return CreateTeamsFromListUseCase(
            self.team_repository,
            self._web_container_manager_dates.get_all_managers_use_case.execute().managers,
            self._app
        )

    @property
    def get_teams_use_case(self) -> GetTeamsUseCase:
        return GetTeamsUseCase(self.team_repository)

    @property
    def get_all_teams_use_case(self) -> GetAllTeamsUseCase:
        return GetAllTeamsUseCase(self.team_repository)

    @property
    def delete_team_use_case(self) -> DeleteTeamUseCase:
        return DeleteTeamUseCase(self.team_repository)
