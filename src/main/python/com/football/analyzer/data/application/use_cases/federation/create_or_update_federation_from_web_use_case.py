import copy
import logging
import threading
from dataclasses import dataclass
from typing import Dict, Any

from flask import current_app

from ...dto.federation_request_dto import CreateOrUpdateFederationFromWebRequestDTO
from main.python.com.football.analyzer.data.application.services.notifications.notification_service import NotificationService
from ....commons.config.config_constants import ConfigConstants
from ....commons.config.config_loader import ConfigLoader
from ....domain.ports.repositories.federation_repository_port import FederationRepositoryPort
from ....infrastructure.adapters.services.web_scrapping_competitions_by_federations_data_source_adapter import (
    WebScrappingCompetitionsByFederationsDataSourceAdapter
)

logger = logging.getLogger(__name__)


@dataclass
class CreateOrUpdateFederationFromWebResult:
    success: bool
    message: str


class CreateOrUpdateFederationFromWebUseCase:

    def __init__(
        self,
        federation_repository: FederationRepositoryPort,
        notification_service: NotificationService,
        app=None
    ):
        self._config_loader = ConfigLoader()
        self._federation_repository = federation_repository
        self._notification_service = notification_service
        self._scraping_adapter = WebScrappingCompetitionsByFederationsDataSourceAdapter()
        self._app = app

    def execute(self, dto: CreateOrUpdateFederationFromWebRequestDTO) -> CreateOrUpdateFederationFromWebResult:
        validation_error = dto.validate()
        if validation_error:
            return CreateOrUpdateFederationFromWebResult(
                success=False,
                message=validation_error
            )
        app = self._app or current_app._get_current_object()

        def background_task():
            with app.app_context():
                try:
                    scraped_data = self._scraping_adapter.get_main_data(dto.competitions_by_federation)
                    for federation_name, federation_data in scraped_data.items():
                        self._federation_repository.save_federation(
                            federation_name, self._prepare_document(federation_data)
                        )
                    self._notification_service.send_success(
                        "Federations Scraping Success",
                        {
                            "Federations processed": len(scraped_data),
                            "Competitions": len(dto.competitions_by_federation)
                        }
                    )
                except Exception as e:
                    self._notification_service.send_error(
                        "Federations Scraping Error",
                        e,
                        {
                            "standings_by_competitions_and_federation": len(dto.competitions_by_federation)
                        }
                    )

        thread = threading.Thread(target=background_task)
        thread.start()
        return CreateOrUpdateFederationFromWebResult(
            success=True,
            message="Scraping process started in background. Data will be updated shortly."
        )

    def _prepare_document(self, federation_data: Dict[str, Any]) -> Dict[str, Any]:
        doc = copy.deepcopy(federation_data)
        competitions_data = ConfigConstants.COMPETITIONS_DATA
        teams_data = ConfigConstants.TEAMS_DATA
        if competitions_data in doc:
            for comp_name, comp_data in doc[competitions_data].items():
                if teams_data in comp_data:
                    doc[competitions_data][comp_name]['teams_count'] = len(comp_data.get(self._config_loader.get_teams_section(), []))
                    del doc[competitions_data][comp_name][teams_data]
        if teams_data in doc:
            del doc[teams_data]
        return doc
