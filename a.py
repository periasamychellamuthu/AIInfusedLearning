import os
from openai import OpenAI
from dotenv import load_dotenv

#load env files from .env environment which is create in hidden file to store api keys
load_dotenv()

#client = OpenAI(
#    api_key=os.getenv("GROQ_API_KEY"),
#    base_url="https://api.groq.com/openai/v1"
#)

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {"role":"system","content":"You are a funny joke teller"},
        {"role":"user", "content":"Tell me a joke"}
    ]
)

print(response.choices[0].message.content)