import logging
from dataclasses import dataclass
from typing import Dict, Any

from src.main.python.com.football.analyzer.data.application.dto.federation_request_dto import GetCalendarsRequestDTO
from src.main.python.com.football.analyzer.data.commons.config.config_constants import ConfigConstants
from src.main.python.com.football.analyzer.data.commons.config.config_loader import ConfigLoader
from src.main.python.com.football.analyzer.data.domain.ports.repositories.federation_repository_port import FederationRepositoryPort

logger = logging.getLogger(__name__)


@dataclass
class GetCalendarsResult:
    success: bool
    message: str
    calendars_by_federation_and_competitions: Dict[str, Dict[str, Any]]


class GetCalendarsUseCase:

    def __init__(self, federation_repository: FederationRepositoryPort):
        self._federation_repository = federation_repository
        self._config_loader = ConfigLoader()

    def execute(self, dto: GetCalendarsRequestDTO) -> GetCalendarsResult:
        validation_error = dto.validate()
        if validation_error:
            return GetCalendarsResult(
                success=False,
                message=validation_error,
                calendars_by_federation_and_competitions={}
            )
        try:
            result = self._get_calendars_by_competition_and_federation(dto)
            return GetCalendarsResult(
                success=True,
                message=f"Retrieved calendars for {len(result)} federations",
                calendars_by_federation_and_competitions=result
            )
        except Exception as e:
            logger.error(f"Error getting calendars: {e}")
            return GetCalendarsResult(
                success=False,
                message=f"Error: {str(e)}",
                calendars_by_federation_and_competitions={}
            )

    def _get_calendars_by_competition_and_federation(self, dto):
        result = {}
        collection = self._federation_repository.get_collection()
        requested = dto.calendars_by_federation_and_competitions
        for federation_name, competition_names in requested.items():
            federation_doc = collection.find_one(
                {ConfigConstants.NAME: federation_name},
                {ConfigConstants.COMPETITIONS_DATA: 1, '_id': 0}
            )
            if not federation_doc:
                logger.warning(f"Federation '{federation_name}' not found in database")
                continue
            calendar_data = self._get_calendar_data(competition_names, federation_doc.get(ConfigConstants.COMPETITIONS_DATA, {}))
            if calendar_data:
                result[federation_name] = calendar_data
        return result

    def _get_calendar_data(self, competition_names, competitions_data):
        fed_result = {}
        for comp_name in competition_names:
            comp_data = competitions_data.get(comp_name, {})
            calendar_section = self._config_loader.get_calendar_section()
            fed_result[comp_name] = {
                calendar_section: comp_data.get(calendar_section, {}),
                ConfigConstants.NUMBER_OF_TEAMS: len(comp_data.get(self._config_loader.get_teams_section(), {}))
            }
        return fed_result
