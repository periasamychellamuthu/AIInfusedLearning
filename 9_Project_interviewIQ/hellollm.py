import sys
import os
from clients import getClient, getModel

client = getClient()
model = getModel()

def ask(prompt):
    response = client.chat.completions.create(model=model, messages=[{"role":"user", "content": prompt}])
    return response.choices[0].message.content

if __name__=="__main__":
    print(ask("hi"))