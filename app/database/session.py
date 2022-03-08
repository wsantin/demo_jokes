from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.declarative import declarative_base

from .base import BaseQuery
from app.configs.environment import Config

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    # poolclass=QueuePool, 
    max_overflow= 40, 
    # pool_pre_ping= Config.SQLALCHEMY_ENGINE_OPTIONS_POOL_PRE_PING,
    pool_timeout = 110,
    pool_size= Config.SQLALCHEMY_ENGINE_OPTIONS_POOL_RECYCLE
)

# engine.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))

SessionLocal = scoped_session(sessionmaker(autocommit=False,
                    autoflush=False,
                    query_cls=BaseQuery,
                    bind=engine))

Base = declarative_base()
Base.query = SessionLocal.query_property()