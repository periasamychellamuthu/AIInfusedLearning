import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_core.prompts import PromptTemplate
from utility.parsers import getStrOutputParser
from utility.web_scraper import fetch_website_content
from utility.models import getGroqLangChainModel
from dotenv import load_dotenv

load_dotenv()

prompt = PromptTemplate.from_template("Give a short, friendly summary of this website:\n\n{website}")

model = getGroqLangChainModel()

parser = getStrOutputParser()

chain = prompt | model | parser

def summarize(url):
    return chain.invoke({"website": fetch_website_content(url)})

if __name__=="__main__":
    print(summarize("https://anthropic.com"))
