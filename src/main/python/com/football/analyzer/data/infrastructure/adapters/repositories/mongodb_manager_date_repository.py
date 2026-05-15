import datetime
import logging
from typing import Dict, Optional

from ....commons.config.config_constants import ConfigConstants
from ....domain.ports.repositories.database_connection_port import DatabaseConnectionPort
from ....domain.ports.repositories.manager_date_repository_port import ManagerDateRepositoryPort

logger = logging.getLogger(__name__)


class MongoDBManagerDateRepository(ManagerDateRepositoryPort):

    COLLECTION_NAME = "manager_dates"

    def __init__(self, db_connection: DatabaseConnectionPort):
        self._db = db_connection
        self._collection = None

    def get_collection(self):
        if self._collection is None:
            self._collection = self._db.get_collection(self.COLLECTION_NAME)
        return self._collection

    def save(self, team_name: str, start_date: str) -> bool:
        try:
            collection = self.get_collection()
            collection.update_one(
                {ConfigConstants.TEAM_NAME: team_name},
                {
                    "$set": {
                        ConfigConstants.MANAGER_START_DATE: start_date,
                        ConfigConstants.UPDATE_AT: datetime.datetime.now()
                    },
                    "$setOnInsert": {
                        ConfigConstants.CREATED_AT: datetime.datetime.now()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save manager date for '{team_name}': {e}")
            return False

    def save_many(self, managers_data: Dict[str, str]) -> Dict[str, bool]:
        results = {}
        for team_name, start_date in managers_data.items():
            results[team_name] = self.save(team_name, start_date)
        return results

    def get(self, team_name: str) -> Optional[str]:
        try:
            collection = self.get_collection()
            result = collection.find_one({ConfigConstants.TEAM_NAME: team_name})
            return result.get(ConfigConstants.MANAGER_START_DATE) if result else None
        except Exception as e:
            logger.error(f"Failed to get manager date for '{team_name}': {e}")
            return None

    def get_all(self) -> Dict[str, str]:
        try:
            collection = self.get_collection()
            cursor = collection.find({}, {"_id": 0, ConfigConstants.TEAM_NAME: 1, ConfigConstants.MANAGER_START_DATE: 1})
            return {doc[ConfigConstants.TEAM_NAME]: doc[ConfigConstants.MANAGER_START_DATE] for doc in cursor}
        except Exception as e:
            logger.error(f"Failed to get all manager dates: {e}")
            return {}

    def delete(self, team_name: str) -> bool:
        try:
            collection = self.get_collection()
            result = collection.delete_one({ConfigConstants.TEAM_NAME: team_name})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete manager date for '{team_name}': {e}")
            return False

    def delete_all(self) -> int:
        try:
            collection = self.get_collection()
            result = collection.delete_many({})
            return result.deleted_count
        except Exception as e:
            logger.error(f"Failed to delete all manager dates: {e}")
            return 0

    def exists(self, team_name: str) -> bool:
        try:
            collection = self.get_collection()
            result = collection.find_one({ConfigConstants.TEAM_NAME: team_name})
            return result is not None
        except Exception as e:
            logger.error(f"Failed to check existence for '{team_name}': {e}")
            return False
