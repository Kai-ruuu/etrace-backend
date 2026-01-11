import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_ENV_PATH = Path(__file__).parent.parent.parent / "app.dev.env"

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_DB_USER: str = "root"
    APP_DB_PASS: str
    APP_DB_HOST: str = "localhost"
    APP_DB_PORT: int = 3306
    APP_DB_NAME: str
    APP_JWT_SECRET_KEY_ALGORITHM: str
    APP_ACCESS_TOKEN_EXPIRY_MINUTES: int
    APP_PASS_RESET_AND_CHANGE_EXPIRY_MINUTES: int
    APP_JWT_PASS_RESET_SECRET_KEY: str
    APP_JWT_AUTHENTICATION_SECRET_KEY: str
    APP_DEFAULT_SYSAD_EMAIL: str
    APP_DEFAULT_SYSAD_PASS: str
    APP_DEFAULT_SYSAD_FIRST_NAME: str
    APP_DEFAULT_SYSAD_LAST_NAME: str

    @property
    def APP_DB_URL(self):
        return f"mysql+asyncmy://{self.APP_DB_USER}:{self.APP_DB_PASS}@{self.APP_DB_HOST}:{self.APP_DB_PORT}/{self.APP_DB_NAME}"
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=APP_ENV_PATH if os.getenv("APP_ENV") != "production" else None,
    )

settings = Settings()