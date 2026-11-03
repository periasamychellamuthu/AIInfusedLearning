import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from strands import Agent
from strands.models.bedrock import BedrockModel
from config import NOVA_LITE

# Nova Lite: Amazon's cheapest model — ideal for a first run.
model = BedrockModel(model_id=NOVA_LITE)

agent = Agent(model=model)

response = agent("Hello! Tell me a fun fact about AI agents.")
print(response)