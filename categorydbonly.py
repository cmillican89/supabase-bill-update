from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://rlswnbbpwqimdpmopdeq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsc3duYmJwd3FpbWRwbW9wZGVxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczOTQ2NzU4OSwiZXhwIjoyMDU1MDQzNTg5fQ.H527W37qqgDp4DVD5hAQCGIA7jk0EkGBRY5d4rPj-MA"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define category keywords
CATEGORY_KEYWORDS = {
    "10C": ["10 commandments", "ten commandments"],
    "Abortion": ["abortion", "fetus", "abortions", "abortion ban", "abortion clinic", "abortion clinic ban", "abortion clinic ban"],
    "Bible in Schools": ["bible", "school", "religious", "scripture", "curriculum"],
    "Chaplains": ["chaplain", "chaplaincy"]
}

# Function to assign a category based on title keywords
def get_category(title):
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if all(keyword in title_lower for keyword in keywords):
            return category
    return None  # No match found

# Fetch all bills from BillDB
response = supabase.table("BillDB").select("bill_id", "title", "category").execute()

if response.data:
    for bill in response.data:
        bill_id = bill["bill_id"]
        title = bill["title"]
        existing_category = bill.get("category")  # Get existing category

        # Determine correct category
        new_category = get_category(title)

        # Update only if category has changed or is missing
        if new_category and new_category != existing_category:
            supabase.table("BillDB").update({"category": new_category}).eq("bill_id", bill_id).execute()
            print(f"✅ Updated Bill {bill_id}: '{title}' → Category: {new_category}")
        else:
            print(f"⚠️ No change needed for Bill {bill_id}: '{title}'")

print("✅ Supabase category assignment completed!")
