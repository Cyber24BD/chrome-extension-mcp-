"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_TIMEOUT: int = 10
    
    # Extension
    EXTENSION_RESPONSE_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
