from scraper import scrape_website
from generate_keywords import generate_seed_keywords

url = "https://en.wikipedia.org/wiki/Search_engine_marketing"   # example site, you can change

print(f"🔎 Scraping website: {url}")
scraped_text = scrape_website(url)
print("\n--- Scraped Text Preview ---")
print(scraped_text[:500], "...\n")  # show first 500 chars only

print("✨ Generating keywords...")
keywords = generate_seed_keywords(scraped_text, n_keywords=10)

print("\n✅ Final Extracted Keywords:")
for kw in keywords:
    print("-", kw)
