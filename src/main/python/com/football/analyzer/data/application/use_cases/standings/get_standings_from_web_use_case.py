import logging
from dataclasses import dataclass
from typing import Dict, Any

from ...dto.standings_request_dto import StandingsRequestDTO
from ....commons.config.config_constants import ConfigConstants
from ....commons.config.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


@dataclass
class GetStandingsFromWebResult:
    success: bool
    message: str
    data: Dict[str, Any]


class GetStandingsFromWebUseCase:

    def __init__(self, federation_repository):
        self._config_loader = ConfigLoader()
        self._federation_repository = federation_repository

    def execute(self, dto: StandingsRequestDTO) -> GetStandingsFromWebResult:
        validation_error = dto.validate()
        if validation_error:
            return GetStandingsFromWebResult(
                success=False,
                message=validation_error,
                data={}
            )
        result = {}
        collection = self._federation_repository.get_collection()
        requested = dto.standings_by_federation_and_competitions
        results_and_standings_section = self._config_loader.get_results_and_standings_section()
        for federation_name, competition_names in requested.items():
            federation_doc = collection.find_one(
                {ConfigConstants.NAME: federation_name},
                {ConfigConstants.COMPETITIONS_DATA: 1, '_id': 0}
            )
            if not federation_doc:
                logger.warning(f"Federation '{federation_name}' not found in database")
                continue
            competitions_data = federation_doc.get(ConfigConstants.COMPETITIONS_DATA, {})
            fed_result = {}
            for comp_name in competition_names:
                comp_data = competitions_data.get(comp_name, {})
                standings_main_url = comp_data.get(results_and_standings_section, {})
                fed_result[comp_name] = {
                    results_and_standings_section: standings_main_url
                }
            if fed_result:
                result[federation_name] = fed_result
        return GetStandingsFromWebResult(
            success=True,
            message=f"Retrieved standings for {len(result)} federations",
            data=result
        )
