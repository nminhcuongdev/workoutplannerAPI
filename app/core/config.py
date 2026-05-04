from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Workout Planner API"
    app_env: str = "development"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    allowed_origins: str = "*"

    @property
    def cors_allowed_origins(self) -> list[str]:
        if self.allowed_origins.strip() == "*":
            return ["*"]
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
