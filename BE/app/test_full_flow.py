from scraper import scrape_website
from generate_keywords import generate_seed_keywords

url = "https://en.wikipedia.org/wiki/Search_engine_marketing"   

print(f"🔎 Scraping website: {url}")
scraped_text = scrape_website(url)

print(scraped_text[:500], "...\n")  

keywords = generate_seed_keywords(scraped_text, n_keywords=10)


for kw in keywords:
    print("-", kw)
