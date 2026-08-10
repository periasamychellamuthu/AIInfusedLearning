import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def getGeminiClient():
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    return client

def getGroqClient():
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
    return client

def getGeminiModel():
    return "gemini-3.6-flash"

def getGroqModel():
    return "llama-3.3-70b-versatile"
