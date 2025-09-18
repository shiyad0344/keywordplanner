from keyword_pipeline import keyword_pipeline
import asyncio
async def main():

    url = "https://www.nike.com/in/w/sale-3yaep"

    # This must be the test account ID (digits only)
    test_customer_id = "1282841519"

    print("🚀 Running keyword pipeline (TEST account)...\n")
    ideas = await keyword_pipeline(url, customer_id=test_customer_id)

    if not ideas:
        print("\n⚠️ No keyword ideas returned. Possible reasons:")
        print(" - Developer token is still in TEST mode (sandbox returns nothing).")
        print(" - Scraper got blocked and text was empty.")
        print(" - Seed keyword generation failed.")
    else:
        print("ideas",ideas)
        print(f"\n🔑 Final Keyword Ideas ({len(ideas)} total):\n")
        for kw in ideas[:]:  # Show top 10
            print(f" {kw['text']} (searches: {kw['avg_monthly_searches']:,})")

if __name__ == "__main__":
    asyncio.run(main())