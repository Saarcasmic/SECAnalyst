"""
Debug Script: Google Revenue Extraction Investigation
This script will:
1. Fetch GOOGL company facts from SEC API
2. List all available us-gaap keys
3. Search for Revenue-related keys
4. Check exact data structure for fiscal year 2023
"""

import json
from retriever import SECDataRetriever

def debug_google_revenue():
    print("=" * 60)
    print("DEBUG: Google Revenue Extraction Investigation")
    print("=" * 60)
    
    retriever = SECDataRetriever()
    cik = "1652044"  # Google/Alphabet CIK
    
    # Step 1: Fetch Company Facts
    print("\n[STEP 1] Fetching company facts for GOOGL (CIK: 1652044)...")
    try:
        facts = retriever.get_company_facts(cik)
        print("✅ Successfully fetched company facts")
    except Exception as e:
        print(f"❌ Failed to fetch: {e}")
        return
    
    # Step 2: Examine Top-Level Structure
    print("\n[STEP 2] Examining top-level structure...")
    print(f"Top-level keys: {list(facts.keys())}")
    
    # Step 3: Get us-gaap keys
    us_gaap = facts.get('facts', {}).get('us-gaap', {})
    print(f"\n[STEP 3] Available us-gaap metrics: {len(us_gaap)} total")
    
    # Step 4: Search for Revenue-related keys
    print("\n[STEP 4] Searching for Revenue-related keys...")
    revenue_keywords = ['revenue', 'sales', 'income']
    matching_keys = []
    
    for key in us_gaap.keys():
        for keyword in revenue_keywords:
            if keyword.lower() in key.lower():
                matching_keys.append(key)
                break
    
    print(f"Found {len(matching_keys)} keys matching revenue/sales/income:")
    for key in sorted(matching_keys)[:30]:  # Show first 30
        print(f"  - {key}")
    
    # Step 5: Check specific keys from our METRIC_ALIASES
    print("\n[STEP 5] Checking keys from METRIC_ALIASES...")
    alias_keys = [
        "Revenues", "Revenue", "TotalRevenue", "TotalRevenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet", "SalesRevenueGoodsNet", "NetRevenues",
        "TotalNetRevenues", "NetSales", "TotalNetSales"
    ]
    
    for key in alias_keys:
        if key in us_gaap:
            print(f"  ✅ '{key}' EXISTS in us-gaap")
            # Get units info
            units = us_gaap[key].get('units', {}).get('USD', [])
            print(f"     -> {len(units)} USD entries found")
            # Show 10-K entries
            ten_k_entries = [u for u in units if u.get('form') == '10-K']
            print(f"     -> {len(ten_k_entries)} are 10-K filings")
            if ten_k_entries:
                print(f"     -> Sample entry: {ten_k_entries[0]}")
        else:
            print(f"  ❌ '{key}' NOT FOUND")
    
    # Step 6: Check for 2023 data specifically
    print("\n[STEP 6] Checking for FY 2023 data...")
    for key in alias_keys:
        if key in us_gaap:
            units = us_gaap[key].get('units', {}).get('USD', [])
            fy2023_entries = [u for u in units if u.get('fy') == 2023]
            if fy2023_entries:
                print(f"  '{key}' FY2023 data:")
                for entry in fy2023_entries:
                    print(f"    - form: {entry.get('form')}, end: {entry.get('end')}, val: {entry.get('val')}")
    
    # Step 7: Dump all revenue-like keys with their sample data
    print("\n[STEP 7] Detailed dump of revenue-like keys...")
    for key in matching_keys:
        if 'revenue' in key.lower():
            metric_data = us_gaap[key]
            units = metric_data.get('units', {}).get('USD', [])
            ten_k_entries = [u for u in units if u.get('form') == '10-K' and u.get('fy') in [2022, 2023, 2024]]
            if ten_k_entries:
                print(f"\n  KEY: '{key}'")
                for entry in ten_k_entries[:5]:
                    print(f"    FY: {entry.get('fy')}, End: {entry.get('end')}, Val: {entry.get('val'):,.0f}")

if __name__ == "__main__":
    debug_google_revenue()
