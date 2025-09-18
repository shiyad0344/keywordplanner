import os
import cohere
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("COHERE_API_KEY not found in environment")

print("COHERE_API_KEY =", os.getenv("COHERE_API_KEY"))

co = cohere.Client(os.getenv("COHERE_API_KEY"))

print("before chat")
response = co.chat(model="command-r", message="Say hello in one word")
print("after chat")

print("RAW:", response)
print("TEXT:", getattr(response, "text", None))
