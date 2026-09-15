import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from models import getGroqLangChainModel, getGroqParser

prompt = ChatPromptTemplate.from_messages([     #from_messages is key here - for template we use from_template
    ("system", "You are friendly tutor"),
    MessagesPlaceholder("history"),
    ("human", "{content}")
])

model = getGroqLangChainModel()

parser = getGroqParser()

chain = prompt | model | parser

# basic example with history
# history = [
#     HumanMessage("Hi, i am periasamy"),
#     AIMessage("Hi periasamy, how can I help you today?")]

# print(chain.invoke({"content": "what is my name", "history": history}))

# conversation chat implementation with history

history = []
while True:
    input_text = input("You: ")
    if input_text.lower() == "exit" or input_text.lower() == "quit":
        break
    response = chain.invoke({"content": input_text, "history": history})
    print("AI: " + response)
    history.append(HumanMessage(input_text))
    history.append(AIMessage(response))
    print(f"history count {len(history)}")

