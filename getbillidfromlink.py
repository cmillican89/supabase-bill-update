import urllib.request
import json
import re

# Your LegiScan API Key
API_KEY = "4baa43fdd1e5d427a54674140afc2699"

# List of Bill URLs
bill_urls = [
    "https://legiscan.com/IN/bill/HB1334/2025",
    "https://legiscan.com/SC/bill/H3537/2025",
    "https://legiscan.com/ND/bill/HB1373/2025",
    "https://legiscan.com/OK/bill/SB456/2025",
    "https://legiscan.com/ID/bill/S1059/2025"
]

# Function to extract state, bill number, and year from URL
def extract_state_bill_year(url):
    match = re.search(r"legiscan\.com/(\w{2})/bill/([\w\d]+)/(\d{4})", url)
    if match:
        state, bill_number, year = match.groups()
        return state, bill_number, int(year)
    else:
        print(f"❌ Invalid URL format: {url}")
        return None, None, None

# Function to get session_id for a given state and year
def get_session_id(state, year):
    session_list_url = f"https://api.legiscan.com/?key={API_KEY}&op=getSessionList&state={state.lower()}"
    try:
        with urllib.request.urlopen(session_list_url) as response:
            data = json.load(response)
            sessions = data.get("sessions", [])
            for session in sessions:
                if session["year_start"] <= year <= session["year_end"]:
                    return session["session_id"]
            print(f"❌ No matching session found for {year} in {state}.")
            return None
    except Exception as e:
        print(f"❌ Failed to fetch session list for {state}: {e}")
        return None

# Function to get bill_id using getMasterList API
def get_bill_id(session_id, bill_number):
    master_list_url = f"https://api.legiscan.com/?key={API_KEY}&op=getMasterList&id={session_id}"
    try:
        with urllib.request.urlopen(master_list_url) as response:
            data = json.load(response)
            masterlist = data.get("masterlist", {})
            for bill_id, bill_data in masterlist.items():
                if isinstance(bill_data, dict) and bill_data.get("number") == bill_number:
                    return bill_id
            print(f"❌ No matching bill found for {bill_number} in session {session_id}.")
            return None
    except Exception as e:
        print(f"❌ Failed to fetch master list for session {session_id}: {e}")
        return None

# Process each URL
for url in bill_urls:
    state, bill_number, year = extract_state_bill_year(url)
    if state and bill_number and year:
        session_id = get_session_id(state, year)
        if session_id:
            bill_id = get_bill_id(session_id, bill_number)
            if bill_id:
                print(f"✅ Bill URL: {url}")
                print(f"   State: {state}")
                print(f"   Bill Number: {bill_number}")
                print(f"   Bill ID: {bill_id}\n")