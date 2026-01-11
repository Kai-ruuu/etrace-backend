import sys
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.utils.logging import Logger
from app.core.settings import settings

# get db url
DB_URL = settings.APP_DB_URL

# ensure that db url was fetched
if not DB_URL:
    Logger.error("APP_DB_URL not found.")
    sys.exit(1)

engine = create_async_engine(
    url=DB_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=1800
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

