from pydantic import BaseModel
from pydantic_settings import BaseSettings

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class DatabaseConfig(BaseModel):
    host: str
    name: str
    user: str
    password: str
    url: str
    async_url: str

    @property
    def migrations_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}@{self.host}/{self.name}"
        )


class RedisConfig(BaseModel):
    host: str
    password: str
    user: str
    user_password: str
    url: str


class Settings(BaseSettings):
    database: DatabaseConfig
    redis: RedisConfig

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()  # type: ignore
