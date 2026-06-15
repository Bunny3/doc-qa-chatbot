import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY","")
    LLM_MODEL: str = os.getenv("LLM_MODEL","llama-3.1-8b-instant")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE",0.7))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS",1024))

    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is  missing from .env")
        print(f" Config loaded - model: {cls.LLM_MODEL}")
    

config = Config()