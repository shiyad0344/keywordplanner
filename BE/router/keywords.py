from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List
from clients.cohere_client import CohereClient

router = APIRouter()
cohere_client = CohereClient()

class KeywordListRequest(BaseModel):
    brand_url: HttpUrl
    brand_competitor_url: HttpUrl
    service_location: List[str]
    shopping_ad_budget: float
    search_ad_budget: float
    pmax_ad_budget: float

class KeywordListResponse(BaseModel):
    success: bool
    keywords: List[str] = []
    message: str = ""

@router.post("/keyword-list", response_model=KeywordListResponse)
async def generate_keywords(request: KeywordListRequest):
    try:
        test_customer_id = "1282841519"
        ideas1=keyword_pipeline(request.brand_url, customer_id=test_customer_id, n_seed_keywords=5)
        ideas2=keyword_pipeline(request.brand_competitor_url, customer_id=test_customer_id, n_seed_keywords=5)

        prompt = f"""
        Generate relevant keywords for a digital marketing campaign with the following details:
        - Brand URL: {request.brand_url}
        - Competitor URL: {request.brand_competitor_url}
        - Service Locations: {', '.join(request.service_location)}
        - Shopping Ad Budget: ${request.shopping_ad_budget}
        - Search Ad Budget: ${request.search_ad_budget}
        - Performance Max Ad Budget: ${request.pmax_ad_budget}
        - Ideas for brand URL (which we get via scraping): {', '.join(ideas1)}
        - Ideas for competitor URL (which we get via scraping): {', '.join(ideas2)}

        Please provide a list of high-value, relevant keywords for this campaign.
        """

        keywords = await cohere_client.generate_keywords(prompt)

        return KeywordListResponse(
            success=True,
            keywords=keywords,
            message="Keywords generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
