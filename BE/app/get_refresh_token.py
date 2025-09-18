

import os
from google_auth_oauthlib.flow import InstalledAppFlow


CLIENT_SECRET_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")


SCOPES = ["https://www.googleapis.com/auth/adwords"]

def main():
    
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)

    
    creds = flow.run_local_server(
        port=8081,          
        prompt="consent"    
              )

    print("working\n")
    print(f"Refresh Token: {creds.refresh_token}")
    print(f"Access Token:  {creds.token}")
    print(f"Expiry:  {creds.expiry}")

if __name__ == "__main__":
    main()
