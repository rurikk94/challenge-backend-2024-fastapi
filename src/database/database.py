import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base

from src.config import config

url: str = f"{config.dbdriver}://{config.dbuser}:{config.dbpass}@{config.dbhost}/{config.dbschema}"

if config.connection_type == "socket":
    url: str = "{}://{}:{}@/{}?unix_socket={}&charset=utf8mb4".format(
        config.dbdriver,
        config.dbuser,
        config.dbpass,
        config.dbschema.replace("/", "%2f")
        .replace(":", "%3a")
        .replace(".", "%2e")
        .replace("-", "%2d"),
        config.dbhost.replace("/", "%2f")
        .replace(":", "%3a")
        .replace(".", "%2e")
        .replace("-", "%2d"),
    )

engine: Engine = create_engine(url, echo=config.dbdebug, pool_size=5, max_overflow=0, pool_timeout=30)

SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()

def get_db() -> Generator[Session, None, None]:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()