import os
from typing import List
import cohere
from dotenv import load_dotenv

from app.test_scraper import content

load_dotenv()

class CohereClient:
    def __init__(self):
        self.client = None

    def _get_client(self):
        if self.client is None:
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                raise ValueError("COHERE_API_KEY environment variable is not set")
            self.client = cohere.Client(api_key=api_key)
        return self.client

    async def generate_keywords(self, prompt: str) -> List[str]:
        try:
            client = self._get_client()

            system_message = """You are a digital marketing keyword expert. Your task is to generate relevant keywords based on the provided information.
    
    IMPORTANT: You MUST respond with ONLY a comma-separated list of keywords. No explanations, no bullet points, no numbering, no additional text.
    
    Format: keyword1, keyword2, keyword3, keyword4, keyword5
    
    Generate 15-20 high-value marketing keywords."""

            response = client.v2.chat(
                model='command-r-08-2024',  # Using available model
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.5,  # Lower temperature for more consistent format
            )
            print("BAJDASJHD",response )
            # Handle different content types in the response
            content_text = ""
            for content_item in response.message.content:
                if hasattr(content_item, 'text') and content_item.text:
                    content_text = content_item.text.strip()
                    break

            if content_text:
                # Remove any potential formatting artifacts
                content_text = content_text.replace('\n', ' ').replace('\r', ' ')

                # Split by comma and clean up
                keywords = [keyword.strip() for keyword in content_text.split(",")]

                # Filter out empty strings and ensure valid keywords
                keywords = [kw for kw in keywords if kw and len(kw.strip()) > 1 and not kw.startswith('-')]

                # Limit to reasonable number
                return keywords[:20]

            return []

        except Exception as e:
            print(f"Error generating keywords: {e}")
            return []

    # async def generate_keywords(self, prompt: str) -> List[str]:
    #     try:
    #         client = self._get_client()
    #
    #         system_message = "You are a digital marketing keyword expert. Generate a list of relevant keywords based on the provided information. Return only the keywords as a comma-separated list, nothing else."
    #
    #         full_prompt = f"{system_message}\n\n{prompt}"
    #
    #         response = client.v2.chat(
    #             model='command-r-08-2024',  # Using available model
    #             messages=[
    #                 {"role": "system", "content": system_message},
    #                 {"role": "user", "content": prompt}
    #             ],
    #             max_tokens=300,
    #             temperature=0.5,
    #         )
    #         print("HUADAWDA",response)
    #         content = response.message.content[0].text.strip()
    #         if content:
    #             keywords = [keyword.strip() for keyword in content.split(",")]
    #             # Clean up keywords - remove empty strings and extra whitespace
    #             keywords = [kw for kw in keywords if kw and len(kw.strip()) > 0]
    #             return keywords
    #         return []
    #     except Exception as e:
    #         print(f"Error generating keywords: {e}")
    #         return []


