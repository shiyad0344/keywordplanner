from app.scraper import scrape_website

url = "https://en.wikipedia.org/wiki/Search_engine_marketing"
content = scrape_website(url)

print("Scraped content preview:\n")
print(content[:500])  
