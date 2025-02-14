import sqlite3

db_path = "legiscan_bills.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the 'url' column exists
cursor.execute("PRAGMA table_info(bills)")
columns = [column[1] for column in cursor.fetchall()]

# Add the 'url' column if it does not exist
if "url" not in columns:
    cursor.execute("ALTER TABLE bills ADD COLUMN url TEXT")
    conn.commit()
    print("✅ 'url' column added to the database.")

conn.close()
print("Database schema updated successfully.")
