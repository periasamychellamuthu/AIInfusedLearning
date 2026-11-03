import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def getClient():
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
    return client

def getModel():
    return "openai/gpt-oss-120b"