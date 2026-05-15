import datetime
import logging
from typing import Any, Dict, List

from ....commons.config.config_constants import ConfigConstants
from ....domain.ports.repositories.database_connection_port import DatabaseConnectionPort
from ....domain.ports.repositories.federation_repository_port import FederationRepositoryPort

logger = logging.getLogger(__name__)


class MongoDBFederationRepository(FederationRepositoryPort):

    COLLECTION_NAME = "federations_countries"

    def __init__(self, db_connection: DatabaseConnectionPort):
        self._db = db_connection
        self._collection = None

    def get_collection(self):
        if self._collection is None:
            self._collection = self._db.get_collection(self.COLLECTION_NAME)
        return self._collection

    def federation_exists(self, federation_name: str) -> bool:
        try:
            collection = self.get_collection()
            result = collection.find_one({ConfigConstants.NAME: federation_name})
            return result is not None
        except Exception as e:
            logger.error(f"Error checking federation existence for '{federation_name}': {e}")
            return False

    def save_federation(self, federation_name: str, federation_data: Dict[str, Any]) -> str:
        try:
            collection = self.get_collection()
            federation_data[ConfigConstants.UPDATE_AT] = datetime.datetime.now()
            if self.federation_exists(federation_name):
                existing = collection.find_one({ConfigConstants.NAME: federation_name})
                if existing and ConfigConstants.TEAMS_DATA in existing and ConfigConstants.TEAMS_DATA not in federation_data:
                    federation_data[ConfigConstants.TEAMS_DATA] = existing.get(ConfigConstants.TEAMS_DATA, {})
                result = collection.update_one(
                    {ConfigConstants.NAME: federation_name},
                    {'$set': federation_data}
                )
                logger.info(f"Updated federation '{federation_name}'")
                return str(existing.get("_id")) if existing.get("_id") else ""
            else:
                federation_data[ConfigConstants.NAME] = federation_name
                result = collection.insert_one(federation_data)
                logger.info(f"Inserted new federation '{federation_name}' with id: {result.inserted_id}")
                return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving federation '{federation_name}': {e}")
            raise

    def save_federations_batch(self, federations_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        results = {}
        for fed_name, fed_data in federations_data.items():
            try:
                fed_id = self.save_federation(fed_name, fed_data)
                results[fed_name] = fed_id
            except Exception as e:
                logger.error(f"Failed to save federation '{fed_name}': {e}")
                results[fed_name] = ""
        return results

    def get_all_federation_names(self) -> List[str]:
        try:
            collection = self.get_collection()
            cursor = collection.find({}, {ConfigConstants.NAME: 1})
            return [doc[ConfigConstants.NAME] for doc in cursor]
        except Exception as e:
            logger.error(f"Error getting all federation names: {e}")
            return []
