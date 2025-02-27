import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    ASSISTANT_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
