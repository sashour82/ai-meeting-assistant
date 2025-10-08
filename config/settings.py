import os

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GPT_MODEL = os.getenv("GPT_MODEL", "gpt-3.5-turbo")

    LANGCHAIN_PROMPT_TEMPLATE = os.getenv(
        "LANGCHAIN_PROMPT_TEMPLATE",
        "Summarize the meeting notes: {text}"
    )

settings = Settings()
