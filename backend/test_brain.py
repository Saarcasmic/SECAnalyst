from orchestrator import Orchestrator
from dotenv import load_dotenv

load_dotenv()

def test_brain():
    print("Initializing Orchestrator...")
    orchestrator = Orchestrator()
    
    try:
        # Test 1: Metric Query
        query1 = "What was Apple's Revenues in 2023?"
        print(f"\n--- Query 1: {query1} ---")
        response1 = orchestrator.handle_query(query1)
        print(response1)
        
        # Test 2: RAG Query
        query2 = "What are the risks regarding competition?"
        print(f"\n--- Query 2: {query2} ---")
        response2 = orchestrator.handle_query(query2)
        print(response2)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        orchestrator.close()

if __name__ == "__main__":
    test_brain()
