import os

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GPT_MODEL = os.getenv("GPT_MODEL", "gpt-3.5-turbo")

settings = Settings()
