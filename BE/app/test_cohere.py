import os
import cohere
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("COHERE_API_KEY not there")


co = cohere.Client(api_key)


response = co.chat(
    model="command-r-plus", 
    message="Write a single sentence describing SEM in very simple terms."
)

print("Cohere Response:", response.text.strip())
