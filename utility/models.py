from utility.config import GROQ_API_KEY, GROQ_BASE_URL

def getGroqModel():
    return "openai/gpt-oss-120b"

def getGeminiModel():
    return "gemini-3.6-flash"

def getGroqLangChainModel(temperature=0.3):
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=getGroqModel(), temperature=temperature, api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)
