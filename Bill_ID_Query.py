# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 23:09:15 2025

@author: steve
"""

import requests
import pandas as pd

# Your LegiScan API Key
API_KEY = '4baa43fdd1e5d427a54674140afc2699'

# Function to get bill_id using getSearch API
def get_bill_id(state, bill_number):
    search_url = 'https://api.legiscan.com/?key='+API_KEY+'&op=getSearch&state='+state+'&bill='+bill_number
    try:
        response = requests.get(search_url)
        data = response.json()
        search_results = data.get('searchresult', [])
        if len(search_results) > 0 :
            return search_results['0']['bill_id']
        print(f'❌ No matching bill found for {bill_number} in {state}.')
        return None
    except Exception as e:
        print(f'❌ Failed to fetch bill data for {bill_number} in {state}: {e}')
        return None

# Example usage
# state = 'ND'
# bill_number = 'HB1373'
# bill_id = get_bill_id(state, bill_number)
# if bill_id:
#      print(f'✅ Bill ID for {state} {bill_number}: {bill_id}')



df = pd.read_excel('bill ID.xlsx')

for index, row in df.iterrows():
    bill_id = get_bill_id(row['state'], row['bill_number'])
    df.loc[index,'bill_id'] = bill_id
try:
    df.to_excel('bill ID.xlsx', index=False)
except Exception as e:
    print("Error writing to file -- make sure it is closed: ", e)

print ("Complete. Queried ", (index+1), " bill IDs")



