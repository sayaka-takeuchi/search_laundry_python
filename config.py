from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url = "mysql+pymysql://root:password@db/search_laundry_python"
    google_application_credentials: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
