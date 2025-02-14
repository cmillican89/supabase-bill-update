import requests
from bs4 import BeautifulSoup
import re

# List of LegiScan Bill URLs
bill_urls = [
    "https://legiscan.com/IN/bill/HB1334/2025",
    "https://legiscan.com/SC/bill/H3537/2025",
    "https://legiscan.com/ND/bill/HB1373/2025",
    "https://legiscan.com/OK/bill/SB456/2025",
    "https://legiscan.com/ID/bill/S1059/2025"
]

def get_bill_id(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch {url}")
        return None

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Look for the `bill_id` in the page source using regex
    script_tags = soup.find_all("script")

    for script in script_tags:
        if script.string and "bill_id" in script.string:
            match = re.search(r'"bill_id":(\d+)', script.string)
            if match:
                return match.group(1)  # Extract the numeric bill_id

    print(f"❌ bill_id not found for {url}")
    return None

# Process each URL
for url in bill_urls:
    bill_id = get_bill_id(url)
    if bill_id:
        print(f"✅ Bill URL: {url}")
        print(f"   Bill ID: {bill_id}\n")
