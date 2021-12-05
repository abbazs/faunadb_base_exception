from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_ADMIN_PYTHON: str
    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    try:
        env_file: str = "./credentials/faunadb.env"
        if Path(env_file).is_file():
            envs = Settings(_env_file=env_file)
        else:
            envs = Settings()
        return envs
    except Exception as e:
        raise e
