import logging
import threading
from dataclasses import dataclass
from typing import Dict

from flask import current_app

from ...dto.federation_request_dto import GetFederationsRequestDTO
from ...services.notification_service import NotificationService
from ....application.dto.team_request_dto import CreateTeamsFromWebRequestDTO
from ....commons.config.config_constants import ConfigConstants
from ....domain.ports.repositories.team_repository_port import TeamRepositoryPort
from ....infrastructure.adapters.services.web_scrapping_team_data_source_adapter import WebScrappingTeamDataSourceAdapter
from ....infrastructure.adapters.services.web_scrapping_team_matches_data_source_adapter import WebScrappingTeamMatchesDataSourceAdapter
from ....infrastructure.container.web_container_federation import WebContainerFederation
from ....infrastructure.container.web_container_manager_dates import WebContainerManagerDates

logger = logging.getLogger(__name__)


@dataclass
class CreateTeamsFromWebResult:
    success: bool
    message: str


class CreateTeamsFromWebUseCase:

    def __init__(self,
                 web_container_manager_dates: WebContainerManagerDates,
                 web_container_federation: WebContainerFederation,
                 team_repository: TeamRepositoryPort,
                 notification_service: NotificationService,
                 app=None):
        self._web_container_federation = web_container_federation
        self._team_repository = team_repository
        self._notification_service = notification_service
        self._app = app
        self._scraping_team_adapter = WebScrappingTeamDataSourceAdapter(
            managers_data=web_container_manager_dates.get_all_managers_use_case.execute().managers
        )
        self._scraping_team_matches_adapter = WebScrappingTeamMatchesDataSourceAdapter(
            managers_data=web_container_manager_dates.get_all_managers_use_case.execute().managers
        )

    def execute(self, dto: CreateTeamsFromWebRequestDTO) -> CreateTeamsFromWebResult:
        validation_error = dto.validate()
        if validation_error:
            return CreateTeamsFromWebResult(
                success=False,
                message=validation_error
            )
        app = self._app or current_app._get_current_object()

        def background_task():
            with app.app_context():
                try:
                    teams_data = self._scraping_team_matches_adapter.get_main_data(
                        self._scraping_team_adapter.get_main_data(
                            self._prepare_teams_data(dto.competitions_by_federation)
                        )
                    )
                    self._team_repository.save_teams_batch(teams_data)
                    self._notification_service.send_success(
                        "Teams Scraping Success",
                        {
                            "Teams processed": len(teams_data),
                            "Competitions": len(dto.competitions_by_federation)
                        }
                    )
                except Exception as e:
                    self._notification_service.send_error(
                        "Teams Scraping Error",
                        e,
                        {
                            "competitions_by_federation": dto.competitions_by_federation
                        }
                    )

        thread = threading.Thread(target=background_task)
        thread.start()
        return CreateTeamsFromWebResult(
            success=True,
            message="Scraping process started in background. Data will be updated shortly."
        )

    def _prepare_teams_data(self, competitions_by_federation: Dict) -> Dict:
        return self._get_all_teams_data(
            self._web_container_federation.get_federations_use_case.execute(
                GetFederationsRequestDTO(
                    competitions_by_federation=self._prepare_federations_data(competitions_by_federation)
                )
            ).federations
        )

    @staticmethod
    def _prepare_federations_data(competitions_by_federation):
        result = {}
        for federation, competitions in competitions_by_federation.items():
            result[federation] = []
            for competition_name, value in competitions.items():
                if value == "ALL" or isinstance(value, list):
                    result[federation].append(competition_name)
        return result

    @staticmethod
    def _get_all_teams_data(federation_data):
        teams_data = {}
        for federation in federation_data:
            competitions = federation[ConfigConstants.COMPETITIONS_DATA]
            for competition in competitions:
                teams = competitions[competition]['Equipos']
                for team in teams:
                    if team not in teams_data:
                        teams_data[team] = teams[team]
        return teams_data
