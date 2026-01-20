import urllib.request
import json
from supabase import create_client, Client
import os

# Supabase credentials (Replace with your own Supabase URL and API key)
SUPABASE_URL = "https://rlswnbbpwqimdpmopdeq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsc3duYmJwd3FpbWRwbW9wZGVxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczOTQ2NzU4OSwiZXhwIjoyMDU1MDQzNTg5fQ.H527W37qqgDp4DVD5hAQCGIA7jk0EkGBRY5d4rPj-MA"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Your LegiScan API Key
API_KEY = "4baa43fdd1e5d427a54674140afc2699"

# List of Bill IDs to Track
BILL_IDS = [
    #ALABAMA
    1957327,1956718,1960841, 2038175,2077783,2038175,2044553,2065940,
    #ARKANSAS
    1949346,1892623,1934832,1968019,
    #ARIZONA
    1937307,1955446,1947047,1937173,1943838,1977391,1949415,1924137,1958309,
    #FLORIDA-- 1-18-26
    2060867, 2060129,2065951,2051942,2069540,2070040,2055841,2045845,2060129,
    2046203,2060867,
    #GEORGIA-- 1-18-26
    1961010,1943206,1964592,1945128,1955587,2083461,
    #IOWA
    1942073,1966347,1973102,
    #IDAHO
    1960196,1959983,1971315, 
    #ILLINOIS   
    1907151,1962942,1971315,2044827,
    #INDIANA-- 1-19-26
    1920665,1911291,1900931,1911676,1904112,1911856,1907654, 2061512,2061478,
    2061503,2065511,2065122,2067221,2056668,
    #KANSAS
    1927874,1936007,
    #KENTUCKY--  1-19-26
    1904677,1910908,1904506,1908069,1955455,1904400,1904381,1967839,1976051,
    2066350,2069012,2067789,2067752,2067909,
    #MARYLAND
    1961127,1961232,1899590,
    #MINNESOTA
    1928057,1937971,1946854,
    #MISSOURI
    1893520,1893866,1894144,1922549,1900908,1896441,1893710,1894019,1945687,
    1932552,1944241,1969621,1966981,1965302,1893628,1948626,1893708,2055430, 
    2054925,2054863,2054635,2054885,2055033,2055922,2056465,2056609,2058959,
    2054874,2055412,2055444,2055860,2055883,
    #MISSISSIPPI-- 1-19-26
    1929982,1910304,1920760,1921686,1930011,1929977,1935864,1911425,1927965,
    2066566,2068161,2069646,2071473,2073625,2073791,2077703,2078219,2084088,
    #MONTANA
    1908731,1946385,
    #NORTH DAKOTA
    1904521,1925513,1930197,1916883,1914843,
    #NEBRASKA
    1934150,1935318,1931467,1934034,1934623,1934460,
    #NEW JERSEY
    1803466,1881878,
    #NEW MEXICO
    1952295,1965537,1978469,1978457,1973942,
    #NEW YORK
    1924860,1931597,
    #OHIO
    1945521, 2047118, 2045358,
    #OKLAHOMA-- 1-18-26
    1922919,1921692,1893340,1910496,1919679,1918936,1907294,1917465,1923010,
    1923772,1893341,1923116,1924151,1918893,2060430,2071267,2073984,2073966,
    2077987,2078114,2078206,2080003,2060383,2065215,2065953,2078221,2078888,
    2078713,2079462,2081285,2080722,2080829,2080591,2082447,2083116,
    #RHODE ISLAND
    1938009,1969046,
    #SOUTH CAROLINA-- 1-19-26
    1896215,1896057,1958934,1896060,1895364,1895655,1895658,1895495,1895439,2059866, 
    2059983,2059853,2059822,2060015,2029713,2029759,2029155,2072603,2073303,2073033,
    2058356,2060019,2059862,
    #SOUTH DAKOTA
    1908661,1919295,
    #TENNESSEE
    1941911,1959971,1959962,1897597,1919383,1942294,1956841,1951112,1952423,1990960,
    2071177,2068885,2080669,2066777,2080669,2085215,1959962,
    #TEXAS
    1890898,1892586,1892228,1963705,1890707,1892186,1943079,1948764,1965965,
    1891586,1946113,
    #US
    1936805,1901919,1916976,
    #VIRGINIA -- 1-19-26
    2085489,2072233,2078759,
    #WASHINGTON
    1963303,
    #WEST VIRGINIA-- 1-19-26
    1979181,1968441,1966855,1971960,1980895,1979003,1977102,1976892,1966758,
    1966755,1972028,1971955,1966276,2079632,2079274,2079393,2078405,2079192,
    2079485,2078972,2081289,2078267,
    #WISCONSIN
    1990954,1994948,2058769,2046609,2056203,2046848,
    #WYOMING
    1896928,1916208,1897604
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
