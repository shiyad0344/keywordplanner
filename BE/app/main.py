from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from keyword_pipeline import keyword_pipeline
from clients.cohere_client import CohereClient
from router.keywords import cohere_client
import random

app = FastAPI(title="SEM Planner Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://keywordplanner1.vercel.app/", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KeywordRequest(BaseModel):
    brand_url: HttpUrl
    brand_competitor_url: HttpUrl
    service_location: List[str]
    shopping_ad_budget: float
    search_ad_budget: float
    pmax_ad_budget: float

class KeywordResponse(BaseModel):
    success: bool
    keywords: List[dict] = []
    
    message: str = ""

@app.get("/")
def root():
    return {"status": "ok", "message": "SEM Planner backend is running"}

@app.post("/api/keyword-list", response_model=KeywordResponse)
async def generate_keywords(request: KeywordRequest):
    try:
        test_customer_id = "1282841519"
        ideas1 =await keyword_pipeline(request.brand_url, customer_id=test_customer_id, n_seed_keywords=5)
        # ideas2 = await keyword_pipeline(request.brand_competitor_url, customer_id=test_customer_id, n_seed_keywords=5)
        # cohere_client = CohereClient()
        # prompt = f"""
        #        Generate relevant keywords for a digital marketing campaign with the following details:
        #        - Brand URL (ours): {request.brand_url}
        #        - Competitor URL: {request.brand_competitor_url}
        #        - Service Locations: {', '.join(request.service_location)}
        #        - Shopping Ad Budget: ${request.shopping_ad_budget}
        #        - Search Ad Budget: ${request.search_ad_budget}
        #        - Performance Max Ad Budget: ${request.pmax_ad_budget}
        #        - Ideas for brand URL (which we get via scraping): {ideas1}
        #        - Ideas for competitor URL (which we get via scraping): {ideas2}

        #        Please provide a list of high-value, relevant keywords for the campaign in the specified location for our brand.
        #        """

        # keywords = await cohere_client.generate_keywords(prompt)
        # keywords_dict = []
        # for keyword_text in keywords:
        #     keywords_dict.append({
        #         "text": keyword_text,
        #         "avg_monthly_searches": _estimate_search_volume(keyword_text)
        #     })
        print("ideas1",ideas1)
        return KeywordResponse(
            success=True,
            keywords=ideas1,
            message="Keywords generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# debug run if invoked directly (optional)

# def _estimate_search_volume( keyword: str) -> int:
#     """Generate realistic search volume estimates"""
#     base_volumes = {
#         'brand': 15000,  # Nike, Adidas
#         'product': 8000,  # shoes, clothing
#         'location': 5000,  # Delhi, Mumbai
#         'modifier': 3000,  # best, tips, guide
#         'generic': 2000  # default
#     }

#     keyword_lower = keyword.lower()

#     # Brand keywords
#     if any(brand in keyword_lower for brand in ['nike', 'adidas']):
#         base = base_volumes['brand']
#     # Product keywords
#     elif any(product in keyword_lower for product in ['shoes', 'clothing', 'sports', 'sneakers']):
#         base = base_volumes['product']
#     # Location keywords
#     elif any(location in keyword_lower for location in ['delhi', 'mumbai']):
#         base = base_volumes['location']
#     # Modifier keywords
#     elif any(modifier in keyword_lower for modifier in ['best', 'tips', 'guide']):
#         base = base_volumes['modifier']
#     else:
#         base = base_volumes['generic']

#     # Add some variation
#     multiplier = random.uniform(0.3, 1.5)
#     volume = int(base * multiplier)

#     # Round to nice numbers
#     if volume > 10000:
#         return round(volume, -3)  # Round to nearest 1000
#     elif volume > 1000:
#         return round(volume, -2)  # Round to nearest 100
#     else:
#         return round(volume, -1)  # Round to nearest 10

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)