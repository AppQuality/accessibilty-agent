import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

    if not OPENAI_API_KEY:
        raise ValueError("No OPENAI_API_KEY found in environment variables.")

config = Config()
