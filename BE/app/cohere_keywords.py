import asyncio
import cohere
import json
import os
from dotenv import load_dotenv

load_dotenv()
print("api")

# 🔑 Replace with your actual Cohere API key
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Initialize async client
co = cohere.AsyncClient(COHERE_API_KEY)
print("api")


async def cohere_keyword_fallback(seeds, n=10):
    """
    Use Cohere to generate keyword ideas + estimated search volumes.
    Returns a list of dicts: [{"keyword": "...", "volume": ...}, ...]
    """
    all_keywords = []

    for seed in seeds:
        prompt = f"""
You are an expert SEO keyword research assistant.

Task:
Given a seed keyword: "{seed}"
1. The seeds are scraped from the website ,so focus only those keyboards which are highly relvant to the given site.
2. Generate 10 highly relevant and semantically related keywords that real users would search for.
3. Include both short-tail and long-tail variations.
4. Assign each keyword an estimated monthly search volume (make them realistic and different).

Return ONLY valid JSON in this format:
{{
  "keywords": [
    {{"text": "keyword1", "avg_monthly_searches": 12000}},
    {{"text": "keyword2", "avg_monthly_searches": 8500}},
    ...
  ]
}}
"""

        # Call Cohere API
        # resp = await co.generate(
        #     model="command-xlarge",
        #     prompt=prompt,
        #     max_tokens=300,
        #     temperature=0.4
        # )
        resp = await co.chat(
            model="command-r-08-2024",
            message=prompt,
            temperature=0,
            response_format={"type": "json_object"}
        )

        raw_text = resp.text
        print("RAW RESPONSE FROM COHERE:", raw_text)



        try:
            # Parse JSON response
           data = json.loads(raw_text)
           all_keywords.extend(data.get("keywords", []))

        except Exception:
            # fallback if parsing fails
            all_keywords.append({"keyword": seed, "volume": 1000})

    return all_keywords


# 🔍 Test the module directly
# if __name__ == "__main__":
#     async def main():
#         seeds = ["flipkart", "online shopping", "seo"]  # example seeds
#         results = await cohere_keyword_fallback(seeds, n=5)

#         print("\n✅ Cohere Keyword Ideas:")
#         # for r in results:
#             # print(f"{r['text']} (volume: {r['avg_monthly_searches']})")
#         print("results",results)

#     asyncio.run(main())
