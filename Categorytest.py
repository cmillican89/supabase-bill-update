import urllib.request
import json
from supabase import create_client, Client
import os

# Supabase credentials
SUPABASE_URL = "https://rlswnbbpwqimdpmopdeq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsc3duYmJwd3FpbWRwbW9wZGVxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczOTQ2NzU4OSwiZXhwIjoyMDU1MDQzNTg5fQ.H527W37qqgDp4DVD5hAQCGIA7jk0EkGBRY5d4rPj-MA"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Your LegiScan API Key
API_KEY = "4baa43fdd1e5d427a54674140afc2699"

# List of Bill IDs to Track
BILL_IDS = [
    1957327, 1937307, 1949346, 1907151, 1920665, 1893520, 1893866, 
    1934150, 1917465, 1925513, 1910496, 1896057, 1919295, 1956841, 
    1959962, 1919679, 1927874, 1890898, 1961127, 1960196, 1941911
]

# Base API URL
base_url = "https://api.legiscan.com/"

# Define categories and their matching keywords
CATEGORY_KEYWORDS = {
    "10C": ["10 commandments", "Ten Commandments"],
    "Abortion": ["abortion", "fetus", "abortions", "abortion ban", "abortion clinic", "abortion clinic ban", "abortion clinic ban"],
    "Bible in Schools": ["bible", "school", "religious", "scripture", "curriculum"],
    "Chaplains": ["chaplain", "chaplaincy"]
}

# Function to assign a category based on title keywords
def get_category(title):
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if all(keyword in title for keyword in keywords):
            return category
    return None  # No match found

# Process each bill
for bill_id in BILL_IDS:
    url = f"{base_url}?key={API_KEY}&op=getBill&id={bill_id}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            bill_info = data.get("bill", {})

            bill_id = bill_info.get("bill_id", "")
            state = bill_info.get("state", "")
            bill_number = bill_info.get("bill_number", "")
            title = bill_info.get("title", "")
            status = bill_info.get("status", "")
            bill_url = bill_info.get("url", "No URL Available")

            # Determine category
            category = get_category(title)

            # Extract most recent action
            history = bill_info.get("history", [])
            if history:
                most_recent_action = history[-1]
                last_action = most_recent_action.get("action", "No actions recorded")
                last_action_date = most_recent_action.get("date", "Unknown date")
            else:
                last_action = "No actions recorded"
                last_action_date = "Unknown date"

            # Check if bill exists in Supabase
            response = supabase.table("BillDB").select("last_action, url, category").eq("bill_id", bill_id).execute()
            existing_bills = response.data

            if existing_bills:
                existing_action = existing_bills[0]["last_action"]
                existing_url = existing_bills[0]["url"]
                existing_category = existing_bills[0].get("category")

                # Update if anything has changed
                if existing_action != last_action or existing_url != bill_url or existing_category != category:
                    supabase.table("BillDB").update({
                        "last_action": last_action,
                        "last_action_date": last_action_date,
                        "url": bill_url,
                        "category": category  # Update category column
                    }).eq("bill_id", bill_id).execute()
                    print(f"🔄 Updated Bill {bill_number}: {last_action} ({last_action_date}), Category: {category}")
            else:
                # Insert new bill with assigned category
                supabase.table("BillDB").insert({
                    "bill_id": bill_id,
                    "state": state,
                    "bill_number": bill_number,
                    "title": title,
                    "status": status,
                    "last_action": last_action,
                    "last_action_date": last_action_date,
                    "url": bill_url,
                    "category": category  # Insert category into the database
                }).execute()
                print(f"📌 Inserted New Bill: {bill_number} - {title} (Category: {category})")

    except Exception as e:
        print(f"❌ Failed to fetch bill {bill_id}: {e}")

print("✅ Supabase database update completed!")
