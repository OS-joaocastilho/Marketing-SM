from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    apify_api_token: str = Field()
    google_api_project: str = Field()
    google_location: str = "us-central1"
    google_text_model: str = "gemini-1.5-pro-001"
