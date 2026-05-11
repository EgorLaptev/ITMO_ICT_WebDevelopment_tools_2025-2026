from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    project_name: str = "Hackathon Management System"
    database_url: str = "postgresql://postgres:123@localhost:5432/hackathon_db"
    jwt_secret: str = "super-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    debug: bool = False
    create_tables_on_startup: bool = True


settings = Settings()
