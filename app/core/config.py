import secrets
from typing import Any, Dict, List, Optional, Union, Tuple
from sqlalchemy.engine import URL

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * x days = x days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    SERVER_NAME: Optional[str] = None
    SERVER_PORT: Optional[int] = 8000
    SERVER_HOST: Optional[AnyHttpUrl] = None
    TICKERS_RANGE_TO_WATCH: Optional[Any] = (0, 100)
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: Optional[str] = ''
    SENTRY_DSN: Optional[HttpUrl] = ''
    MONGO_URL: Optional[str] = ''

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    SQL_SERVER: Optional[str] = None
    SQL_USER: Optional[str] = None
    SQL_PASSWORD: Optional[str] = None
    SQL_DB: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Optional[Any] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return URL.create(
            "mssql+pyodbc",
            username=values.get("SQL_USER"),
            password=values.get("SQL_PASSWORD"),
            host=values.get("SQL_SERVER"),
            port=1433,
            database=values.get("SQL_DB"),
            query={
                "driver": "ODBC Driver 17 for SQL Server",
            },
        )

    @validator("PROJECT_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        print('------------------------------------------------------------------------------------------------------')
        print(values)
        if not v:
            return values["PROJECT_NAME"]
        return v

    @validator("MONGO_URL")
    def get_mongo_url(cls, v: Optional[str], values: Dict[str, Any]):
        return values.get("MONGO_URL")

    @validator("TICKERS_RANGE_TO_WATCH")
    def get_tickers_range_to_watch(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        value = values.get('TICKERS_RANGE_TO_WATCH') if not v else v
        in_range = list(value.split('-'))
        range_tuple = tuple([int(in_range[0]), int(in_range[1])])
        return range_tuple

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
