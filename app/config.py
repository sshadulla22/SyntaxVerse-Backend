from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./notes.db"
    
    # App Configuration
    APP_NAME: str = "ANCText API"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = "your-very-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    
    # CORS Configuration
    # Can be a comma-separated string in .env
    ALLOWED_ORIGINS: str = "*"

    @property
    def parsed_origins(self) -> List[str]:
        if self.ALLOWED_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
