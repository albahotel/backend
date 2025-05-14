from pydantic_settings import BaseSettings

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    db_url: str
    user: str
    password: str
    host: str
    name: str
    echo: bool = False
    
    @property
    def migrations_url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}/{self.name}" 
    
    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8" 

settings = Settings()  # type: ignore
