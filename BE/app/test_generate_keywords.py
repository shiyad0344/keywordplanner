from generate_keywords import generate_seed_keywords

print("🔎 Generating seed keywords from sample text...")
# Example scraped text (you can replace this with real scraped content later)
sample_text = """
Search Engine Marketing (SEM) is a form of internet marketing that involves 
the promotion of websites by increasing their visibility in search engine results 
pages (SERPs) primarily through paid advertising. 
It helps businesses reach potential customers at the right time.
"""

print("🔎 Generating seed keywords from sample text...")

keywords = generate_seed_keywords(sample_text, n_keywords=5)

print("✅ Extracted Keywords:")
for kw in keywords:
    print("-", kw)
