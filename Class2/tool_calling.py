import json
import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import gradio as gr
from clients import getGroqClient, getGroqModel
client = getGroqClient()

# response = client.chat.completions.create(
#     model=getGroqModel(),
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "What is the capital of France?"}]);

# print(response.choices[0].message.content)


PRICES = {"shoes": 799, "hat": 399, "bag": 1420, "shorts": 1299, "pants": 1699}

def get_price(item):
    print(f"Getting price for {item}...")
    return f"{PRICES.get(item, 'Item not found')}"

tool = [
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "Get the price of an item from the store.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The name of the item to get the price for."
                    }
                },
                "required": ["item"]
            }
        }
    }
]

def ask(user_message):
    message = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]
    response = client.chat.completions.create(
        model=getGroqModel(),
        messages=message,
        tools=tool
    )
    msg = response.choices[0].message

    if msg.tool_calls:
        message.append(msg)
        for call in msg.tool_calls:
            # sample payload : {"name": "get_price", "arguments": {"item":"headphones"}}
            args = json.loads(call.function.arguments)
            result = get_price(args["item"])
            message.append({"role": "tool", "tool_call_id": call.id, "content": result})
        response = client.chat.completions.create(model=getGroqModel(), messages=message)
        msg = response.choices[0].message

    return msg.content

# print(ask("What is the price of shoes?"))
# print(ask("What is the price of belt?"))
# print(ask("What is the capital of France?"))

def chat(message, history):
    return ask(message)

gr.ChatInterface(fn=chat, title="Groq LLM with Tool Calling").launch()