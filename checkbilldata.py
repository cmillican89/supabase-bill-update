import urllib.request
import json

API_KEY = "4baa43fdd1e5d427a54674140afc2699"
BILL_ID = 302  # Test with one bill first

base_url = "https://api.legiscan.com/"
url = f"{base_url}?key={API_KEY}&op=getBill&id={BILL_ID}"

try:
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        print(json.dumps(data, indent=4))  # Pretty print the API response
except Exception as e:
    print(f"❌ Failed to fetch bill {BILL_ID}: {e}")
