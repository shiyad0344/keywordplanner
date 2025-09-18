# app/get_refresh_token.py

import os
from google_auth_oauthlib.flow import InstalledAppFlow

# Path to your OAuth2 client_secret.json (downloaded from Google Cloud Console)
CLIENT_SECRET_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")

# Scopes required for Google Ads API
SCOPES = ["https://www.googleapis.com/auth/adwords"]

def main():
    # Create the OAuth2 flow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)

    # Run local server to handle the redirect automatically
    creds = flow.run_local_server(
        port=8081,          # Must match your redirect URI in Google Cloud Console
        prompt="consent"    # Always force account chooser
    )

    print("\n✅ Success! Here are your tokens:\n")
    print(f"Refresh Token: {creds.refresh_token}")
    print(f"Access Token:  {creds.token}")
    print(f"Expiry:        {creds.expiry}")

if __name__ == "__main__":
    main()
