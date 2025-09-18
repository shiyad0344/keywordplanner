from keyword_pipeline import keyword_pipeline
import asyncio
async def main():

    url = "https://www.nike.com/in/w/sale-3yaep"


    test_customer_id = "1282841519"

    ideas = await keyword_pipeline(url, customer_id=test_customer_id)

    if not ideas:
        print("No ideas")
        
    else:
        print("ideas",ideas)
        
        for kw in ideas[:]: 
            print(f" {kw['text']} (searches: {kw['avg_monthly_searches']:,})")

if __name__ == "__main__":
    asyncio.run(main())