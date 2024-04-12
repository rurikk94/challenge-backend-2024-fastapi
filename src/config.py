from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Challenge-API"
    app_version: str = "240328"
    debug: bool = False
    dbdebug: bool = False

    connection_type: str = "tcp"
    dbdriver: str = "postgresql+psycopg2"
    dbuser: str = "user"
    dbpass: str = "password"
    dbhost: str = "localhost:5432"
    dbschema: str = "challenge"

    port: int = 8000

    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    version: str = "240411.2"


config = Settings()
