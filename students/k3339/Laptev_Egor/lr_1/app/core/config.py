from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Hackathon Management System"
    database_url: str = "postgresql://postgres:123@localhost:5432/hackathon_db"
    jwt_secret: str = "super-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    debug: bool = False
    create_tables_on_startup: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
