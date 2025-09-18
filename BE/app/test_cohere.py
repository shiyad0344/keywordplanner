import os
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("COHERE_API_KEY not found in environment")

# Initialize Cohere client
co = cohere.Client(api_key)

# Use chat() instead of generate()
response = co.chat(
    model="command-r-plus",  # works with chat()
    message="Write a single sentence describing SEM in very simple terms."
)

print("Cohere Response:", response.text.strip())
