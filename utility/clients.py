from openai import OpenAI
from utility.config import GROQ_API_KEY, GEMINI_API_KEY, GROQ_BASE_URL, GEMINI_BASE_URL

def getGroqClient():
    return OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

def getGeminiClient():
    return OpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_BASE_URL)

def getGoogleGenAIClient():
    from google import genai
    return genai.Client(api_key=GEMINI_API_KEY)
