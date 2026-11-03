import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utility.clients import getGoogleGenAIClient

client = getGoogleGenAIClient()

for m in client.models.list():
    if "generateContent" in m.supported_actions:
        print(m.name)
