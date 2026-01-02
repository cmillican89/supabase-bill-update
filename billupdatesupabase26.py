import urllib.request
import json
from supabase import create_client, Client
import os

# Supabase credentials (Replace with your own Supabase URL and API key)
SUPABASE_URL = "https://gjkofljwjmfopqlrqjet.supabase.co"
SUPABASE_KEY = "sb_secret_7OJm4iTLvvib0fg8JFXE7w_F-h_0x7X"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Your LegiScan API Key
API_KEY = "4baa43fdd1e5d427a54674140afc2699"

# List of Bill IDs to Track
BILL_IDS = [
    #ALABAMA
    2038175,
    #ARKANSAS
    
    #ARIZONA
    
    #GEORGIA
    
    #IOWA
    
    #IDAHO
     
    #ILLINOIS   
    
    #INDIANA
    2061512,
    #KANSAS
    
    #KENTUCKY
    
    #MARYLAND
    
    #MINNESOTA
    
    #MISSOURI
    
    #MISSISSIPPI
    
    #MONTANA
    
    #NORTH DAKOTA
    
    #NEBRASKA
    
    #NEW JERSEY
    
    #NEW MEXICO
    
    #NEW YORK
    
    #OHIO
    2047118, 2045358,
    #OKLAHOMA
    
    #RHODE ISLAND
    
    #SOUTH CAROLINA
    2059866,
    #SOUTH DAKOTA
    
    #TENNESSEE
     
    #TEXAS
    
    #US
    
    #WASHINGTON
    
    #WEST VIRGINIA
    
    #WYOMING
    
    # Add all your bill IDs here...
]

base_url = "https://api.legiscan.com/"
updated_bills = []

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
            
            # Extract most recent action
            history = bill_info.get("history", [])
            if history:
                most_recent_action = history[-1]  # Last entry is most recent action
                last_action = most_recent_action.get("action", "No actions recorded")
                last_action_date = most_recent_action.get("date", "Unknown date")
            else:
                last_action = "No actions recorded"
                last_action_date = "Unknown date"

            # Check if bill exists in Supabase
            response = supabase.table("BillDB").select("last_action, url").eq("bill_id", bill_id).execute()
            existing_bills = response.data

            if existing_bills:
                existing_action = existing_bills[0]["last_action"]
                existing_url = existing_bills[0]["url"]
                
                # If last action or URL has changed, update the database
                if existing_action != last_action or existing_url != bill_url:
                    supabase.table("BillDB").update({
                        "last_action": last_action,
                        "last_action_date": last_action_date,
                        "url": bill_url
                    }).eq("bill_id", bill_id).execute()
                    print(f"🔄 Updated Bill {bill_number}: {last_action} ({last_action_date})")
            else:
                # If bill doesn't exist, insert it
                supabase.table("BillDB").insert({
                    "bill_id": bill_id,
                    "state": state,
                    "bill_number": bill_number,
                    "title": title,
                    "status": status,
                    "last_action": last_action,
                    "last_action_date": last_action_date,
                    "url": bill_url
                }).execute()
                print(f"📌 Inserted New Bill: {bill_number} - {title}")
    
    except Exception as e:
        print(f"❌ Failed to fetch bill {bill_id}: {e}")

print("✅ Supabase database update completed!")
