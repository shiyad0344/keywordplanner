from generate_keywords import generate_seed_keywords

print("genrating")

sample_text = """
Search Engine Marketing (SEM) is a form of internet marketing that involves 
the promotion of websites by increasing their visibility in search engine results 
pages (SERPs) primarily through paid advertising. 
It helps businesses reach potential customers at the right time.
"""



keywords = generate_seed_keywords(sample_text, n_keywords=5)

for kw in keywords:
    print("-", kw)
