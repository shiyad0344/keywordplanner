

from google.ads.googleads.client import GoogleAdsClient         
from google.ads.googleads.errors import GoogleAdsException
import yaml
from cohere_keywords import cohere_keyword_fallback

from scraper import scrape_website
from generate_keywords import generate_seed_keywords


def get_keyword_ideas(client, customer_id, seeds):
    """Fetch keyword ideas from Google Ads API."""
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.keyword_seed.keywords.extend(seeds)
    request.geo_target_constants.append(
        "geoTargetConstants/2840" 
    )
    request.language = "languageConstants/1000"  
    request.include_adult_keywords = False

    response = keyword_plan_idea_service.generate_keyword_ideas(request=request)

    ideas = []
    for idea in response:
        ideas.append({
            "text": idea.text,
            "avg_monthly_searches": idea.keyword_idea_metrics.avg_monthly_searches
        })

    return ideas


async def keyword_pipeline(url, customer_id=None, n_seed_keywords=5):
    """End-to-end pipeline: scrape -> seed keywords -> keyword ideas."""
    print(f"🔍 Extracting seed keywords from: {url}")

    
    text = scrape_website(url)
    print(f"✅ Scraped text length: {len(text)}")

    
    seeds = generate_seed_keywords(text, n_seed_keywords)
    print(f"✅ Seed Keywords: {seeds}")


    # client = GoogleAdsClient.load_from_storage("./app/google-ads.yaml")

    # if not customer_id:
    #     with open('./app/google-ads.yaml', 'r') as f:
    #         config = yaml.safe_load(f)
    #     customer_id = str(config['login_customer_id'])



    ideas = await cohere_keyword_fallback(seeds, n=5)
    # print("ideas",ideas)
    return ideas

    