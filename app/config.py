from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    api_key: str = Field(..., env="API_KEY")

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    redis_db: int = Field(..., env="REDIS_DB")
    redis_pass: str = Field(..., env="REDIS_PASS")
    redis_test_url: str = "redis://localhost:6380"

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
