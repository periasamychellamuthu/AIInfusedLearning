import os
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(REPO_ROOT / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
