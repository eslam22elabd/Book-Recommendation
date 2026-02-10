from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "Book Recommendation API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Gemini Configuration
    API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # Google Books API
    GOOGLE_BOOKS_API_URL: str = "https://www.googleapis.com/books/v1/volumes"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
