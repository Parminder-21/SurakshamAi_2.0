from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # LLM
    openai_api_key: str = ""
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    google_api_key: str = ""
    groq_api_key: str = ""
    llm_provider: str = "groq"
    llm_model: str = "llama-3.3-70b-versatile"

    # External APIs
    google_safe_browsing_api_key: str = ""

    # Firebase / Supabase
    firebase_credentials_path: str = "firebase-credentials.json"
    supabase_url: str = ""
    supabase_key: str = ""

    # App
    app_env: str = "development"
    secret_key: str = "change-me"
    allowed_origins: str = "http://localhost:3000"
    rate_limit_per_minute: int = 30

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
