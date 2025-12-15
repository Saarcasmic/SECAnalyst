"""
Reproduction Script: Google Revenue vs Revenues
"""
from repository import FinancialDataRepository
from retriever import SECDataRetriever
from database import get_db_session

def reproduction():
    print("=" * 60)
    print("REPRODUCTION: Metric Name Sensitivity")
    print("=" * 60)
    
    session = next(get_db_session())
    retriever = SECDataRetriever()
    repo = FinancialDataRepository(session, retriever)
    
    # Test 1: "Revenue" (Singular) - Should Work
    print("\n[TEST 1] Fetching GOOGL 'Revenue' for 2023...")
    res1 = repo.get_metric("GOOGL", "Revenue", 2023)
    print(f"Result: {res1}")

    # Test 2: "Revenues" (Plural) - Suspected Failure
    print("\n[TEST 2] Fetching GOOGL 'Revenues' for 2023...")
    res2 = repo.get_metric("GOOGL", "Revenues", 2023)
    print(f"Result: {res2}")
    
    session.close()

if __name__ == "__main__":
    reproduction()
