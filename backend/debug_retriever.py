import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def debug_sec_tags():
    cik = "0000320193" # Apple
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    
    headers = {
        "User-Agent": os.getenv("USER_AGENT", "Name Email@example.com") 
    }
    
    print(f"Fetching data from {url}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        us_gaap = data.get('facts', {}).get('us-gaap', {})
        print(f"Found {len(us_gaap)} keys in us-gaap.")
        
        print("\n--- Keys containing 'Revenue' ---")
        for key in us_gaap.keys():
            if "Revenue" in key:
                print(f"- {key}")
                
        print("\n--- Inspecting 'Revenues' Key ---")
        if 'Revenues' in us_gaap:
            units = us_gaap['Revenues'].get('units', {}).get('USD', [])
            print(f"Found {len(units)} entries for 'Revenues'. First 3:")
            for entry in units[:3]:
                print(json.dumps(entry, indent=2))
                
            # Print latest 3 as well since we are interested in recent data
            print("... Last 3:")
            for entry in units[-3:]:
                print(json.dumps(entry, indent=2))
        else:
            print("'Revenues' key NOT found.")

        print("\n--- Inspecting 'RevenueFromContractWithCustomerExcludingAssessedTax' Key ---")
        alt_key = 'RevenueFromContractWithCustomerExcludingAssessedTax'
        if alt_key in us_gaap:
             units = us_gaap[alt_key].get('units', {}).get('USD', [])
             print(f"Found {len(units)} entries for '{alt_key}'. Last 3:")
             for entry in units[-3:]:
                print(json.dumps(entry, indent=2))
        else:
             print(f"'{alt_key}' key NOT found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_sec_tags()
