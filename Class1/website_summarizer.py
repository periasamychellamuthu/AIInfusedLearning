import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from website_scraper import fetch_website_content
from clients import getGeminiClient
from clients import getGeminiModel

client = getGeminiClient()
system_prompt = """You analyze the contents of a website and
give a short, friendly summary. Ignore navigation menus.
Respond in markdown."""

def summarize(url):
    website = fetch_website_content(url)
    response = client.chat.completions.create(
        model=getGeminiModel(),
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":f"Summarize this website:\n\n{website}"}
        ]
    )
    return response.choices[0].message.content