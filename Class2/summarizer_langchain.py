import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Class1.website_scraper import fetch_website_content
from models import getGroqLangChainModel
from dotenv import load_dotenv

load_dotenv()

prompt = PromptTemplate.from_template("Give a short, friendly summary of this website:\n\n{website}")

model = getGroqLangChainModel()
# model = ChatGoogleGenerativeAI(model=getGeminiModel())

parser = StrOutputParser()

chain = prompt | model | parser

def summarize(url):
    return chain.invoke({"website": fetch_website_content(url)})

if __name__=="__main__":
    print(summarize("https://anthropic.com"))
