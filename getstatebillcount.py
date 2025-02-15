from supabase import create_client, Client

# Supabase Credentials
SUPABASE_URL = "https://rlswnbbpwqimdpmopdeq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsc3duYmJwd3FpbWRwbW9wZGVxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczOTQ2NzU4OSwiZXhwIjoyMDU1MDQzNTg5fQ.H527W37qqgDp4DVD5hAQCGIA7jk0EkGBRY5d4rPj-MA"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Call the RPC function
response = supabase.rpc("get_bill_count_per_state").execute()

# Convert results to dictionary {state: bill_count}
state_bill_counts = {row["state"]: row["bill_count"] for row in response.data}

print(state_bill_counts)  # Example output: {'NY': 12, 'TX': 25, 'CA': 40}
