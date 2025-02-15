import gspread
from supabase import create_client, Client

# Supabase Credentials
SUPABASE_URL = "https://rlswnbbpwqimdpmopdeq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsc3duYmJwd3FpbWRwbW9wZGVxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczOTQ2NzU4OSwiZXhwIjoyMDU1MDQzNTg5fQ.H527W37qqgDp4DVD5hAQCGIA7jk0EkGBRY5d4rPj-MA"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Connect to Google Sheets without credentials
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1c7S54GJ1tMguivekkpnFpQXEOuk5Y9oicIQl0CfhhuU/edit?usp=sharing"
gc = gspread.oauth()  # This will prompt a web-based OAuth login (first-time setup)
sheet = gc.open_by_url(GOOGLE_SHEET_URL).sheet1  # Open the first sheet

# Fetch data from Supabase
response = supabase.table("BillDB").select("*").execute()
bills = response.data

# Clear existing data
sheet.clear()

# Define headers
headers = ["bill_id", "state", "bill_number", "title", "status", "last_action", "last_action_date", "url", "category"]
sheet.append_row(headers)

# Insert data
for bill in bills:
    row = [
        bill.get("bill_id", ""),
        bill.get("state", ""),
        bill.get("bill_number", ""),
        bill.get("title", ""),
        bill.get("status", ""),
        bill.get("last_action", ""),
        bill.get("last_action_date", ""),
        bill.get("url", ""),
        bill.get("category", ""),
    ]
    sheet.append_row(row)

print("✅ Google Sheets updated successfully!")
