import os
import cohere
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def generate_seed_keywords(text: str, n_keywords: int = 10):
    """
    Use Cohere to extract top seed keywords from scraped text.
    """
    prompt = f"""
    Extract {n_keywords} important seed keywords from this text.
    Return them as a simple list, separated by commas.

    Text:
    {text[:1500]}
    """

    response = co.chat(model="command-r-plus-08-2024", message=prompt)

    # Get the raw output
    keywords_text = getattr(response, "text", "").strip()
    print("RAW RESPONSE:", keywords_text)  # Debugging

    if not keywords_text:
        return ["⚠️ No keywords generated"]

    # Handle both commas and newlines
    keywords = [kw.strip("-• \n") for kw in keywords_text.replace("\n", ",").split(",") if kw.strip()]
    return keywords
