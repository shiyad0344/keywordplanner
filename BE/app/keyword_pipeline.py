# # app/keyword_pipeline.py
#
# from google.ads.googleads.client import GoogleAdsClient
# from google.ads.googleads.errors import GoogleAdsException
# import yaml
#
# from app.scraper import scrape_website
# from app.generate_keywords import generate_seed_keywords
#
#
# def get_keyword_ideas(client, customer_id, seeds):
#     """Fetch keyword ideas from Google Ads API."""
#     keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
#
#     request = client.get_type("GenerateKeywordIdeasRequest")
#     request.customer_id = customer_id
#     request.keyword_seed.keywords.extend(seeds)
#     request.geo_target_constants.append(
#         "geoTargetConstants/2840"  # United States
#     )
#     request.language = "languageConstants/1000"  # English
#     request.include_adult_keywords = False
#
#     response = keyword_plan_idea_service.generate_keyword_ideas(request=request)
#
#     ideas = []
#     for idea in response:
#         ideas.append({
#             "text": idea.text,
#             "avg_monthly_searches": idea.keyword_idea_metrics.avg_monthly_searches
#         })
#
#     return ideas
#
#
# def keyword_pipeline(url, customer_id=None, n_seed_keywords=5):
#     """End-to-end pipeline: scrape -> seed keywords -> keyword ideas."""
#     print(f"🔍 Extracting seed keywords from: {url}")
#
#     # Step 1: Scrape content
#     text = scrape_website(url)
#     print(f"✅ Scraped text length: {len(text)}")
#
#     # Step 2: Generate seed keywords from content
#     seeds = generate_seed_keywords(text, n_seed_keywords)
#     print(f"✅ Seed Keywords: {seeds}")
#
#     # Step 3: Load Google Ads config
#     client = GoogleAdsClient.load_from_storage("./app/google-ads.yaml")
#
#     # Step 4: Get customer ID (from parameter or YAML file)
#     if not customer_id:
#         with open('./app/google-ads.yaml', 'r') as f:
#             config = yaml.safe_load(f)
#         customer_id = str(config['login_customer_id'])
#
#     print(f"✅ Using Customer ID: {customer_id}")
#
#     # Step 5: Request keyword ideas with fallback
#     try:
#         ideas = get_keyword_ideas(client, customer_id, seeds)
#         if not ideas:  # Empty response due to test token
#             raise Exception("No keyword ideas returned - likely test token")
#         return ideas
#     except Exception as e:
#         print(f"⚠️  Google Ads API Error: {str(e)}")
#         print("📝 Using mock keyword data (developer token restrictions)")
#
#         # Generate mock keyword ideas based on seed keywords
#         mock_ideas = []
#         base_searches = [15000, 8500, 5200, 3300, 2100, 1600, 1000, 850, 650, 450]
#
#         for i, seed in enumerate(seeds):
#             # Clean seed keyword (remove numbers and dots)
#             clean_seed = seed.replace("1. ", "").replace("2. ", "").replace("3. ", "").replace("4. ", "").replace("5. ", "")
#             mock_ideas.extend([
#                 {"text": clean_seed, "avg_monthly_searches": base_searches[i % len(base_searches)]},
#                 {"text": f"{clean_seed} tips", "avg_monthly_searches": base_searches[i % len(base_searches)] // 2},
#                 {"text": f"best {clean_seed}", "avg_monthly_searches": base_searches[i % len(base_searches)] // 3},
#                 {"text": f"{clean_seed} guide", "avg_monthly_searches": base_searches[i % len(base_searches)] // 4},
#             ])
#
#         return mock_ideas[:20]  # Return top 20 mock ideas

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
        "geoTargetConstants/2840"  # United States
    )
    request.language = "languageConstants/1000"  # English
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

    # Step 1: Scrape content
    text = scrape_website(url)
    print(f"✅ Scraped text length: {len(text)}")

    # Step 2: Generate seed keywords from content
    seeds = generate_seed_keywords(text, n_seed_keywords)
    print(f"✅ Seed Keywords: {seeds}")

    # Step 3: Load Google Ads config
    # client = GoogleAdsClient.load_from_storage("./app/google-ads.yaml")

    # Step 4: Get customer ID (from parameter or YAML file)
    # if not customer_id:
    #     with open('./app/google-ads.yaml', 'r') as f:
    #         config = yaml.safe_load(f)
    #     customer_id = str(config['login_customer_id'])

    # print(f"✅ Using Customer ID: {customer_id}")

    # Step 5: Request keyword ideas with fallback

    ideas = await cohere_keyword_fallback(seeds, n=5)
    # print("ideas",ideas)
    return ideas

    # try:
    #     ideas = get_keyword_ideas(client, customer_id, seeds)
    #     if not ideas:  # Empty response due to test token
    #         raise Exception("No keyword ideas returned - likely test token")
    #     return ideas
    # except Exception as e:
    #     print(f"⚠️  Google Ads API Error: {str(e)}")
    #     print("📝 Using mock keyword data (developer token restrictions)")

    #     # Generate mock keyword ideas based on seed keywords
    #     mock_ideas = []
    #     base_searches = [15000, 8500, 5200, 3300, 2100, 1600, 1000, 850, 650, 450]

    #     for i, seed in enumerate(seeds):
    #         # Clean seed keyword (remove numbers and dots)
    #         clean_seed = seed.replace("1. ", "").replace("2. ", "").replace("3. ", "").replace("4. ", "").replace("5. ", "")
    #         mock_ideas.extend([
    #             {"text": clean_seed, "avg_monthly_searches": base_searches[i % len(base_searches)]},
    #             {"text": f"{clean_seed} tips", "avg_monthly_searches": base_searches[i % len(base_searches)] // 2},
    #             {"text": f"best {clean_seed}", "avg_monthly_searches": base_searches[i % len(base_searches)] // 3},
    #             {"text": f"{clean_seed} guide", "avg_monthly_searches": base_searches[i % len(base_searches)] // 4},
    #         ])

    #     return mock_ideas[:20]  # Return top 20 mock ideas