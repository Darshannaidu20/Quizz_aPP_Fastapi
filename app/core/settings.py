import secrets
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Student Quiz App"
    # ENVIRONMENT: str = "dev"

    ECHO_SQL: bool = False
    USE_ALEMBIC: bool = False
    USE_SQLITE: bool = False
    USE_MYSQL: bool = True  

    MYSQL_BASE: str = "mysql+aiomysql"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "Darshan#123"
    MYSQL_DB: str = "test"
    MYSQL_SERVER: str = "localhost"
    MYSQL_PORT: int = 3306

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MIN: int = 30

   
    model_config = SettingsConfigDict()

    def get_db_url(self) -> str:
        """
        Get the appropriate database URL based on configuration.
        """
        if self.USE_MYSQL:
            return (
                f"{self.MYSQL_BASE}://"
                f"{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
                f"@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
            )



settings = Settings()


print(settings.get_db_url())

@lru_cache
def get_settings() -> Settings:
    return settings