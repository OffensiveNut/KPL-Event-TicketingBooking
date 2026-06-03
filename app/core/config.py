from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str = Field(default=...)
    db_port: int = Field(default=...)
    db_user: str = Field(default=...)
    db_password: str = Field(default=...)
    db_name: str = Field(default=...)
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
