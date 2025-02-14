import sqlite3
import urllib.request
import json

# Your LegiScan API Key
API_KEY = "4baa43fdd1e5d427a54674140afc2699"

# List of Bill IDs to Track (39 Bills)
BILL_IDS = [
    1957327, 1937307, 1949346, 1907151, 1920665, 1893520, 1893866, 
    1934150, 1917465, 1925513, 1910496, 1896057, 1919295, 1956841, 
    1959962, 1919679, 1927874, 1890898, 1961127, 
    1960196, 1941911, 1929982, 1959971, 1892586, 1892228, 
    1963705, 1922919, 1942073, 1908731, 1896215, 1896057,
    1921692, 1904521, 1908661, 1893340, 1961232, 1956718, 1961010, 1911291,
1900931, 1892623, 1930197, 1894144, 1896928, 1963303, 1899590, 1911676, 1922549, 1935318, 1904677, 1910908, 1936805, 1900908, 1896441, 1893710, 1894019, 1945687, 1958934, 1803466, 1881878, 1896060, 1955446, 1901919, 1947047, 1924860, 1904112, 1910304, 1938009, 1937173, 1916208, 1962942, 1895364, 1918936, 1907294, 1931467, 1897604, 1931597, 1952295, 1911856, 1895655, 1916883, 1959983, 1895658, 1943206, 1946385, 1934034, 1895495, 1943838, 1907654, 1904506, 1908069, 1932552, 1944241, 1920760, 1921686, 1930011, 1929977, 1935864, 1914843, 1934623, 1945521, 1895439, 1897597, 1919383, 1942294, 1890707, 1892186, 1943079, 1948764, 1934832, 1955455, 1928057 
]

base_url = "https://api.legiscan.com/"
db_path = "legiscan_bills.db"

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Table if Not Exists (Ensures URL is included)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        bill_id INTEGER PRIMARY KEY,
        state TEXT,
        bill_number TEXT,
        title TEXT,
        status INTEGER,
        last_action TEXT,
        last_action_date TEXT,
        url TEXT
    )
""")

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
            bill_url = bill_info.get("url", "No URL Available")  # Ensure the URL is retrieved

            # Extract the most recent action from the history array
            history = bill_info.get("history", [])
            if history:
                most_recent_action = history[-1]  # Last entry is the most recent action
                last_action = most_recent_action.get("action", "No actions recorded")
                last_action_date = most_recent_action.get("date", "Unknown date")
            else:
                last_action = "No actions recorded"
                last_action_date = "Unknown date"

            # Debugging Print Statements (Ensures URL is Pulled Correctly)
            print(f"✅ Bill {bill_number} ({state}): Latest Action - {last_action} on {last_action_date}")
            print(f"🔗 URL Retrieved: {bill_url}")

            # Check if bill exists and if last_action or URL has changed
            cursor.execute("SELECT last_action, url FROM bills WHERE bill_id = ?", (bill_id,))
            existing_bill = cursor.fetchone()

            if existing_bill:
                existing_action, existing_url = existing_bill
                # If last_action or URL has changed, update the database
                if existing_action != last_action or existing_url != bill_url:
                    cursor.execute("""
                        UPDATE bills 
                        SET last_action = ?, last_action_date = ?, url = ?
                        WHERE bill_id = ?
                    """, (last_action, last_action_date, bill_url, bill_id))
                    print(f"🔄 Updated Bill {bill_number}: New Action -> {last_action}, New URL -> {bill_url}")
                    updated_bills.append((bill_id, state, bill_number, title, status, last_action, last_action_date, bill_url))
            else:
                # If bill does not exist, insert it
                cursor.execute("""
                    INSERT INTO bills (bill_id, state, bill_number, title, status, last_action, last_action_date, url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (bill_id, state, bill_number, title, status, last_action, last_action_date, bill_url))
                print(f"📌 Inserted New Bill: {bill_number} - {title}")
                updated_bills.append((bill_id, state, bill_number, title, status, last_action, last_action_date, bill_url))

    except Exception as e:
        print(f"❌ Failed to fetch bill {bill_id}: {e}")

conn.commit()
conn.close()

print("Database update completed ✅")

