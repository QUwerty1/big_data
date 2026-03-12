from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API settings
    api_base_url: str = "http://localhost:5031/"
    api_timeout: int = 30
    
    # Auth settings
    token_file: str = "/home/mrquw/.token"
    
    class Config:
        env_prefix = "STORAGE_"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_api_url() -> str:
    """Get the base API URL"""
    return settings.api_base_url.rstrip('/')


def get_token_file() -> str:
    """Get the token file path"""
    return settings.token_file