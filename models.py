import sys
import os

from dotenv import load_dotenv

load_dotenv()

def getGroqLangChainModel():
    from langchain_openai import ChatOpenAI
    model = ChatOpenAI(model="openai/gpt-oss-120b", temperature=0.3, api_key=os.getenv("GROQ_API_KEY"),base_url="https://api.groq.com/openai/v1")
    return model

def getGroqParser():
    from langchain_core.output_parsers import StrOutputParser
    return StrOutputParser()

def getHuggingFaceEmdedderModelName():
    return "all-MiniLM-L6-v2";

def getCrossEncoderModel():
    return "cross-encoder/ms-marco-MiniLM-L6-v2";