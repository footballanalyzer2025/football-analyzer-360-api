import logging
from typing import Any, Dict, List, Optional

from ....commons.config.config_constants import ConfigConstants
from ....domain.ports.repositories.database_connection_port import DatabaseConnectionPort
from ....domain.ports.repositories.team_repository_port import TeamRepositoryPort

logger = logging.getLogger(__name__)


class MongoDBTeamRepository(TeamRepositoryPort):

    COLLECTION_NAME = "teams"

    def __init__(self, db_connection: DatabaseConnectionPort):
        self._db = db_connection
        self._collection = None

    def get_collection(self):
        if self._collection is None:
            self._collection = self._db.get_collection(self.COLLECTION_NAME)
        return self._collection

    def team_exists(self, team_name: str) -> bool:
        try:
            return self.get_collection().find_one({ConfigConstants.NAME: team_name}) is not None
        except Exception as e:
            logger.error(f"Error checking team existence for '{team_name}': {e}")
            return False

    def save_team(self, team_name: str, team_data: Dict[str, Any]) -> str:
        try:
            collection = self.get_collection()
            if self.team_exists(team_name):
                result = collection.update_one(
                    {ConfigConstants.NAME: team_name},
                    {'$set': team_data}
                )
                logger.info(f"Updated team '{team_name}'")
                return str(result.upserted_id) if result.upserted_id else ""
            else:
                team_data[ConfigConstants.NAME] = team_name
                result = collection.insert_one(team_data)
                logger.info(f"Inserted new team '{team_name}'")
                return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving team '{team_name}': {e}")
            raise

    def save_teams_batch(self, teams_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        results = {}
        for team_name, team_data in teams_data.items():
            try:
                team_id = self.save_team(team_name, team_data)
                results[team_name] = team_id
            except Exception as e:
                logger.error(f"Failed to save team '{team_name}': {e}")
                results[team_name] = ""
        return results

    def get_all_team_names(self) -> List[str]:
        try:
            collection = self.get_collection()
            cursor = collection.find({}, {ConfigConstants.TEAM_NAME: 1})
            return [doc[ConfigConstants.TEAM_NAME] for doc in cursor]
        except Exception as e:
            logger.error(f"Error getting all team names: {e}")
            return []

    def logical_delete_team(self, team_name: str) -> bool:
        try:
            collection = self.get_collection()
            result = collection.update_one(
                {ConfigConstants.TEAM_NAME: team_name},
                {'$unset': {k: "" for k in [ConfigConstants.HAS_MANAGER_DATA,
                                            ConfigConstants.MANAGER_START_DATE,
                                            ConfigConstants.SECTIONS,
                                            ConfigConstants.MATCHES,
                                            ConfigConstants.CREATED_AT,
                                            ConfigConstants.UPDATE_AT]
                            },
                 '$set': {'is_deleted': True}
                 }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error deleting team '{team_name}': {e}")
            return False

    def find_by_name(self, team_name: str) -> Optional[Dict[str, Any]]:
        try:
            collection = self.get_collection()
            return collection.find_one({ConfigConstants.TEAM_NAME: team_name}, {'_id': 0})
        except Exception as e:
            logger.error(f"Error finding team '{team_name}': {e}")
            return None
