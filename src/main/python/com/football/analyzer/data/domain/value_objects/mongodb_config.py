import os
from dataclasses import dataclass


@dataclass(frozen=True)
class MongoDBConfig:

    host: str
    port: int
    username: str
    password: str
    database_name: str
    auth_source: str = "admin"

    @property
    def uri(self) -> str:
        return f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/?authSource={self.auth_source}"

    @classmethod
    def from_env(cls) -> 'MongoDBConfig':
        return cls(
            host=os.getenv('MONGO_HOST', 'localhost'),
            port=int(os.getenv('MONGO_PORT', 27017)),
            username=os.getenv('MONGO_ROOT_USER', 'football_admin'),
            password=os.getenv('MONGO_ROOT_PASSWORD', 'football_secure_password_2024'),
            database_name=os.getenv('MONGO_DATABASE', 'football_analyzer'),
            auth_source=os.getenv('MONGO_AUTH_SOURCE', 'admin')
        )
