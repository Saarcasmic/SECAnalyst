"""
Test Script: Verify Google Revenue Extraction Fix
"""
from repository import FinancialDataRepository
from retriever import SECDataRetriever
from database import get_db_session

def test_google_revenue():
    print("=" * 60)
    print("TEST: Google Revenue Extraction")
    print("=" * 60)
    
    session = next(get_db_session())
    retriever = SECDataRetriever()
    repo = FinancialDataRepository(session, retriever)
    
    # Test GOOGL Revenue for 2023
    print("\n[TEST 1] Fetching GOOGL Revenue for 2023...")
    try:
        result = repo.get_metric("GOOGL", "Revenue", 2023)
        print(f"Result: {result}")
        if "307,394" in str(result).replace(",", "").replace("000000", ""):
            print("✅ SUCCESS: Found correct value (~$307B)")
        elif "Data not found" in result:
            print("❌ FAILED: Data not found")
        else:
            print(f"⚠️ UNEXPECTED: Got {result}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test AAPL Revenue for 2023
    print("\n[TEST 2] Fetching AAPL Revenue for 2023...")
    try:
        result = repo.get_metric("AAPL", "Revenue", 2023)
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test MSFT Revenue for 2023
    print("\n[TEST 3] Fetching MSFT Revenue for 2023...")
    try:
        result = repo.get_metric("MSFT", "Revenue", 2023)
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    session.close()

if __name__ == "__main__":
    test_google_revenue()
