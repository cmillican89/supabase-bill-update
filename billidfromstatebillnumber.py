# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 23:09:15 2025

@author: steve
"""

import requests

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
state = 'WI'
bill_number = 'AB103'
bill_id = get_bill_id(state, bill_number)
if bill_id:
     print(f'✅ Bill ID for {state} {bill_number}: {bill_id}')

state = 'WI'
bill_number = 'SB120'
bill_id = get_bill_id(state, bill_number)
if bill_id:
     print(f'✅ Bill ID for {state} {bill_number}: {bill_id}')

state = 'WI'
bill_number = 'SB734'
bill_id = get_bill_id(state, bill_number)
if bill_id:
     print(f'✅ Bill ID for {state} {bill_number}: {bill_id}')

state = 'WI'
bill_number = 'AB546'
bill_id = get_bill_id(state, bill_number)
if bill_id:
     print(f'✅ Bill ID for {state} {bill_number}: {bill_id}')

state = 'WI'
bill_number = 'AB718'
bill_id = get_bill_id(state, bill_number)
if bill_id:
     print(f'✅ Bill ID for {state} {bill_number}: {bill_id}')

state = 'WI'
bill_number = 'SB553'
bill_id = get_bill_id(state, bill_number)
if bill_id:
     print(f'✅ Bill ID for {state} {bill_number}: {bill_id}')
