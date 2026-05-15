import logging
from dataclasses import dataclass
from typing import List, Dict, Any

from ....domain.ports.repositories.team_repository_port import TeamRepositoryPort

logger = logging.getLogger(__name__)


@dataclass
class GetAllTeamsResult:
    success: bool
    count: int
    teams: List[Dict[str, Any]]


class GetAllTeamsUseCase:

    def __init__(self, team_repository: TeamRepositoryPort):
        self._team_repository = team_repository

    def execute(self) -> GetAllTeamsResult:
        try:
            collection = self._team_repository.get_collection()
            cursor = collection.find({}, {'_id': 0})
            teams = list(cursor)

            return GetAllTeamsResult(
                success=True,
                count=len(teams),
                teams=teams
            )

        except Exception as e:
            logger.error(f"Error getting all teams: {e}")
            return GetAllTeamsResult(
                success=False,
                count=0,
                teams=[]
            )
