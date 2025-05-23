import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_KEY: str = os.getenv("OPENAI_KEY")

    if not OPENAI_KEY:
        raise ValueError("No OPENAI_KEY found in environment variables.")

config = Config()
