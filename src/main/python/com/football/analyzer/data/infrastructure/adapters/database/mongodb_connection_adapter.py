import logging
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError, CollectionInvalid

from ....domain.ports.repositories.database_connection_port import DatabaseConnectionPort
from ....domain.value_objects.mongodb_config import MongoDBConfig


class MongoDBConnectionAdapter(DatabaseConnectionPort):

    def __init__(self, config: Optional[MongoDBConfig] = None):
        self._config = config or MongoDBConfig.from_env()
        self._client: Optional[MongoClient] = None
        self._db = None
        self._is_connected = False
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def connect(self) -> bool:
        try:
            self._client = MongoClient(
                self._config.uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            self._client.admin.command('ping')
            self._db = self._client[self._config.database_name]
            self._is_connected = True
            self.logger.info(f"Connected to MongoDB at {self._config.host}:{self._config.port}")
            self.logger.info(f"Using database: {self._config.database_name}")
            return True
        except ConnectionFailure as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            self._is_connected = False
            return False

    def disconnect(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            self._is_connected = False
            self.logger.info("Disconnected from MongoDB")

    def is_connected(self) -> bool:
        if not self._is_connected or not self._client:
            return False
        self._client.admin.command('ping')
        return True
    
    def get_collection(self, collection_name: str) -> Any:
        if not self.is_connected():
            self.connect()
        return self._db[collection_name]

    def create_collection(self, collection_name: str, capped: bool = False, size: int = None, max_documents: int = None) -> bool:
        try:
            if not self.is_connected():
                self.connect()
            if collection_name in self._db.list_collection_names():
                self.logger.warning(f"Collection '{collection_name}' already exists")
                return False
            options = {}
            if capped:
                options['capped'] = True
                if size:
                    options['size'] = size
                if max_documents:
                    options['max'] = max_documents
            self._db.create_collection(collection_name, **options)
            self.logger.info(f"Collection '{collection_name}' created successfully")
            return True
        except CollectionInvalid as e:
            self.logger.error(f"Invalid collection configuration for '{collection_name}': {e}")
            return False
        except PyMongoError as e:
            self.logger.error(f"Failed to create collection '{collection_name}': {e}")
            return False

    def collection_exists(self, collection_name: str) -> bool:
        try:
            if not self.is_connected():
                self.connect()
            return collection_name in self._db.list_collection_names()
        except PyMongoError as e:
            self.logger.error(f"Failed to check collection existence '{collection_name}': {e}")
            return False

    def list_collections(self) -> List[str]:
        try:
            if not self.is_connected():
                self.connect()
            return self._db.list_collection_names()
        except PyMongoError as e:
            self.logger.error(f"Failed to list collections: {e}")
            return []

    def drop_collection(self, collection_name: str) -> bool:
        try:
            if not self.is_connected():
                self.connect()
            if collection_name not in self._db.list_collection_names():
                self.logger.warning(f"Collection '{collection_name}' does not exist")
                return False
            self._db[collection_name].drop()
            self.logger.info(f"Collection '{collection_name}' dropped successfully")
            return True
        except PyMongoError as e:
            self.logger.error(f"Failed to drop collection '{collection_name}': {e}")
            return False

    def rename_collection(self, old_name: str, new_name: str, drop_target: bool = False) -> bool:
        try:
            if not self.is_connected():
                self.connect()
            if old_name not in self._db.list_collection_names():
                self.logger.warning(f"Collection '{old_name}' does not exist")
                return False
            if new_name in self._db.list_collection_names():
                if drop_target:
                    self._db[new_name].drop()
                    self.logger.info(f"Dropped existing collection '{new_name}'")
                else:
                    self.logger.warning(f"Collection '{new_name}' already exists and drop_target is False")
                    return False
            self._db[old_name].rename(new_name)
            self.logger.info(f"Collection renamed from '{old_name}' to '{new_name}'")
            return True
        except PyMongoError as e:
            self.logger.error(f"Failed to rename collection from '{old_name}' to '{new_name}': {e}")
            return False

    def collection_stats(self, collection_name: str) -> Dict:
        try:
            if not self.is_connected():
                self.connect()
            if collection_name not in self._db.list_collection_names():
                self.logger.warning(f"Collection '{collection_name}' does not exist")
                return {}
            stats = self._db.command('collstats', collection_name)
            return {
                'name': collection_name,
                'count': stats.get('count', 0),
                'size': stats.get('size', 0),
                'avg_obj_size': stats.get('avgObjSize', 0),
                'storage_size': stats.get('storageSize', 0),
                'total_index_size': stats.get('totalIndexSize', 0),
                'indexes': stats.get('nindexes', 0),
                'capped': stats.get('capped', False)
            }
        except PyMongoError as e:
            self.logger.error(f"Failed to get stats for collection '{collection_name}': {e}")
            return {}

    def insert_one(self, collection_name: str, document: Dict) -> str:
        try:
            collection = self.get_collection(collection_name)
            result = collection.insert_one(document)
            self.logger.info(f"Inserted document into {collection_name}: {result.inserted_id}")
            return str(result.inserted_id)
        except PyMongoError as e:
            self.logger.error(f"Failed to insert document into {collection_name}: {e}")
            raise

    def insert_many(self, collection_name: str, documents: List[Dict]) -> List[str]:
        try:
            collection = self.get_collection(collection_name)
            result = collection.insert_many(documents)
            self.logger.info(f"Inserted {len(result.inserted_ids)} documents into {collection_name}")
            return [str(unique_id) for unique_id in result.inserted_ids]
        except PyMongoError as e:
            self.logger.error(f"Failed to insert documents into {collection_name}: {e}")
            raise

    def find(self, collection_name: str, query: Dict = None, projection: Dict = None) -> List[Dict]:
        try:
            collection = self.get_collection(collection_name)
            cursor = collection.find(query or {}, projection or {})
            return list(cursor)
        except PyMongoError as e:
            self.logger.error(f"Failed to find documents in {collection_name}: {e}")
            return []

    def find_one(self, collection_name: str, query: Dict = None, projection: Dict = None) -> Optional[Dict]:
        try:
            collection = self.get_collection(collection_name)
            return collection.find_one(query or {}, projection or {})
        except PyMongoError as e:
            self.logger.error(f"Failed to find document in {collection_name}: {e}")
            return None

    def update_one(self, collection_name: str, query: Dict, update: Dict) -> int:
        try:
            collection = self.get_collection(collection_name)
            result = collection.update_one(query, {'$set': update})
            self.logger.info(f"Updated {result.modified_count} document in {collection_name}")
            return result.modified_count
        except PyMongoError as e:
            self.logger.error(f"Failed to update document in {collection_name}: {e}")
            return 0

    def delete_one(self, collection_name: str, query: Dict) -> int:
        try:
            collection = self.get_collection(collection_name)
            result = collection.delete_one(query)
            self.logger.info(f"Deleted {result.deleted_count} document from {collection_name}")
            return result.deleted_count
        except PyMongoError as e:
            self.logger.error(f"Failed to delete document from {collection_name}: {e}")
            return 0

    def delete_many(self, collection_name: str, query: Dict) -> int:
        try:
            collection = self.get_collection(collection_name)
            result = collection.delete_many(query)
            self.logger.info(f"Deleted {result.deleted_count} documents from {collection_name}")
            return result.deleted_count
        except PyMongoError as e:
            self.logger.error(f"Failed to delete documents from {collection_name}: {e}")
            return 0

    @property
    def config(self) -> MongoDBConfig:
        return self._config

    @property
    def database_name(self) -> str:
        return self._config.database_name
    