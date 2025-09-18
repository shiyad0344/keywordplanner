# app/test_google_ads.py

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def main():
    # Load credentials from google-ads.yaml
    client = GoogleAdsClient.load_from_storage("./app/google-ads.yaml")

    # Replace with your own customer ID (without dashes)
    customer_id = 8397145923

    try:
        ga_service = client.get_service("GoogleAdsService")

        # Simple query: get the first 5 campaigns
        query = """
            SELECT campaign.id, campaign.name
            FROM campaign
            ORDER BY campaign.id
            LIMIT 5
        """

        response = ga_service.search(customer_id=customer_id, query=query)

        print("\n✅ Campaigns in your account:\n")
        for row in response:
            print(f"Campaign ID: {row.campaign.id}, Name: {row.campaign.name}")

    except GoogleAdsException as ex:
        print(f"Request failed with status {ex.error.code().name}")
        for error in ex.failure.errors:
            print(f"\tError: {error.message}")

if __name__ == "__main__":
    main()
