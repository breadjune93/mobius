from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET: str = "mobius_systems"
    JWT_ALG: str = "HS256"
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    DATABASE_URL: str = ""

    class Config:
        env_file = ".env"

settings = Settings()