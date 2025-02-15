import urllib.request
import json
import psycopg2
import os

# Digital Ocean PostgreSQL credentials
DB_HOST = "64.23.139.80"  # Example: db-postgresql-nyc1-12345-do-user-7890.db.ondigitalocean.com
DB_PORT = "5432"  # Default for Digital Ocean's PostgreSQL
DB_NAME = "tst"
DB_USER = "orpheus.gaur"
DB_PASSWORD = "FOcZKr8ATjGmPe{"

# LegiScan API Key
API_KEY = "4baa43fdd1e5d427a54674140afc2699"

# List of Bill IDs to Track
BILL_IDS = [
    #ALABAMA
    1957327,1956718,1960841,
    #ARKANSAS
    1949346,1892623,1934832,
    #ARIZONA
    1937307,1955446,1947047,1937173,1943838,
    #GEORGIA
    1961010,1943206,
    #IOWA
    1942073,1966347,
    #IDAHO
    1960196,1959983,1971315,
    #ILLINOIS   
    1907151,1962942,1971315,
    #INDIANA
    1920665,1911291,1900931,1911676,1904112,1911856,1907654,
    #KANSAS
    1927874,
    #KENTUCKY
    1904677,1910908,1904506,1908069,1955455,1904400,1904381,
    #MARYLAND
    1961127,1961232,1899590,
    #MINNESOTA
    1928057,1937971,1946854,
    #MISSOURI
    1893520,1893866,1894144,1922549,1900908,1896441,1893710,1894019,1945687,
    1932552,1944241,
    #MISSISSIPPI
    1929982,1910304,1920760,1921686,1930011,1929977,1935864,1911425,
    #MONTANA
    1908731,1946385,
    #NORTH DAKOTA
    1904521,1925513,1930197,1916883,1914843,
    #NEBRASKA
    1934150,1935318,1931467,1934034,1934623,
    #NEW JERSEY
    1803466,1881878,
    #NEW MEXICO
    1952295,
    #NEW YORK
    1924860,1931597,
    #OHIO
    1945521,
    #OKLAHOMA
    1922919,1921692,1893340,1910496,1919679,1918936,1907294,1917465,
    #RHODE ISLAND
    1938009,
    #SOUTH CAROLINA
    1896215,1896057,1958934,1896060,1895364,1895655,1895658,1895495,1895439,
    #SOUTH DAKOTA
    1908661,1919295,
    #TENNESSEE
    1941911,1959971,1959962,1897597,1919383,1942294,1956841,
    #TEXAS
    1890898,1892586,1892228,1963705,1890707,1892186,1943079,1948764,1965965,
    1891586,1946113,
    #US
    1936805,1901919,1916976,
    #WASHINGTON
    1963303,
    #WYOMING
    1896928,1916208,1897604
    # Add more bill IDs here...
]

base_url = "https://api.legiscan.com/"

# Connect to PostgreSQL (Target `src` schema)
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True  # Ensure automatic commits
    cursor = conn.cursor()
    print("✅ Connected to Digital Ocean PostgreSQL (Schema: src)")
except Exception as e:
    print(f"❌ Failed to connect to PostgreSQL: {e}")
    exit()

# Function to insert/update bills in `src.bill`
def upsert_bill(bill_data):
    sql = """
    INSERT INTO src.billdb (bill_id, state, bill_number, title, status, last_action, last_action_date, url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (bill_id) 
    DO UPDATE SET 
        last_action = EXCLUDED.last_action,
        last_action_date = EXCLUDED.last_action_date,
        url = EXCLUDED.url;
    """
    cursor.execute(sql, (
        bill_data["bill_id"],
        bill_data["state"],
        bill_data["bill_number"],
        bill_data["title"],
        bill_data["status"],
        bill_data["last_action"],
        bill_data["last_action_date"],
        bill_data["url"]
    ))
    print(f"📌 Upserted Bill {bill_data['bill_number']} - {bill_data['title']}")

# Process each bill
for bill_id in BILL_IDS:
    url = f"{base_url}?key={API_KEY}&op=getBill&id={bill_id}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            bill_info = data.get("bill", {})

            bill_data = {
                "bill_id": bill_info.get("bill_id", ""),
                "state": bill_info.get("state", ""),
                "bill_number": bill_info.get("bill_number", ""),
                "title": bill_info.get("title", ""),
                "status": bill_info.get("status", ""),
                "url": bill_info.get("url", "No URL Available"),
                "last_action": "No actions recorded",
                "last_action_date": "Unknown date"
            }

            # Extract most recent action
            history = bill_info.get("history", [])
            if history:
                most_recent_action = history[-1]  # Last entry is the most recent action
                bill_data["last_action"] = most_recent_action.get("action", "No actions recorded")
                bill_data["last_action_date"] = most_recent_action.get("date", "Unknown date")

            # Insert or update bill
            upsert_bill(bill_data)

    except Exception as e:
        print(f"❌ Failed to fetch bill {bill_id}: {e}")

# Close DB connection
cursor.close()
conn.close()
print("✅ PostgreSQL (src.billdb) update completed!")
