import logging
import threading
from dataclasses import dataclass
from typing import Dict

from flask import current_app

from .get_teams_use_case import GetTeamsUseCase
from ....application.dto.team_request_dto import CreateTeamsFromListRequestDTO, GetTeamsRequestDTO
from ....commons.config.config_constants import ConfigConstants
from ....domain.ports.repositories.team_repository_port import TeamRepositoryPort
from ....infrastructure.adapters.services.web_scrapping_team_data_source_adapter import WebScrappingTeamDataSourceAdapter

logger = logging.getLogger(__name__)


@dataclass
class CreateTeamsFromListResult:
    success: bool
    message: str


class CreateTeamsFromListUseCase:

    def __init__(
            self,
            team_repository: TeamRepositoryPort,
            managers_data: Dict[str, str],
            app=None
    ):
        self._team_repository = team_repository
        self._get_teams_use_case = GetTeamsUseCase(self._team_repository)
        self._app = app
        self._scraping_team_adapter = WebScrappingTeamDataSourceAdapter(managers_data=managers_data)

    def execute(self, dto: CreateTeamsFromListRequestDTO) -> CreateTeamsFromListResult:
        validation_error = dto.validate()
        if validation_error:
            return CreateTeamsFromListResult(
                success=False,
                message=validation_error
            )
        app = self._app or current_app._get_current_object()

        def background_task():
            with app.app_context():
                try:
                    teams_to_create = dto.teams_to_create
                    all_teams = self._get_teams_use_case.execute(GetTeamsRequestDTO(teams_to_create)).data
                    teams_to_process = {}
                    for team_name in teams_to_create:
                        if team_name in all_teams and all_teams[team_name].get(ConfigConstants.MAIN_URL):
                            teams_to_process[team_name] = all_teams[team_name]
                    teams_data = self._scraping_team_adapter.get_main_data(teams_to_process)
                    self._team_repository.save_teams_batch(teams_data)
                    logger.info(f"Scraping completed. Processed {len(teams_data)} teams")
                except Exception as e:
                    logger.error(f"Background task failed: {e}")

        thread = threading.Thread(target=background_task)
        thread.start()
        return CreateTeamsFromListResult(
            success=True,
            message="Scraping process started in background. Data will be updated shortly."
        )
