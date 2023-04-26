from __future__ import annotations
from functools import lru_cache
from urllib.parse import urlparse
import typing as t

from pydantic import BaseSettings, validator
from pydantic.networks import MultiHostDsn
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase


class MySQLDsn(MultiHostDsn):
    __slots__ = ()

    allowed_schemes = {
        'mysql',
        'mysql+pymysql',
        'mysql+aiomysql',
        'mysql+asyncmy',
    }
    user_required = True


class SQLASettings(BaseSettings):
    password: t.Optional[str]
    database_uri: MySQLDsn

    @validator('database_uri')
    def prepare_dsn(cls, v, values) -> MySQLDsn:
        password = values.get('password')

        if password is None:
            return v

        dsn = urlparse(v)
        return MySQLDsn(
            None,
            scheme=dsn.scheme,
            user=dsn.username,
            password=values['password'],
            host=dsn.hostname,
            port=dsn.port,
            path=dsn.path,
        )

    class Config:
        env_prefix = 'SQLALCHEMY_'
        secrets_dir = '/run/secrets'
        fields = {
            'password': {
                'env': ['db_user_password', f'{env_prefix}password']
            }
        }


@lru_cache()
def get_db_settings() -> SQLASettings:
    return SQLASettings()


engine = create_async_engine(
    get_db_settings().database_uri,
    # 'mysql+asyncmy://user:resu@mysql/podnosi-api',
    # pool_size=100,
    # max_overflow=200,
)
SessionLocal = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as session:
        yield session
