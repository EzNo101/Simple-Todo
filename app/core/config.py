from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SECRET_KEY: str

    CACHE_TTL: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"
        

settings = Settings()