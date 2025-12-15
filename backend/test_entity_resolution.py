"""
Test Script: Entity Resolution Logic
"""
import asyncio
from orchestrator import Orchestrator

async def test_normalization():
    print("=" * 60)
    print("TEST: Entity Resolution Normalization")
    print("=" * 60)
    
    orch = Orchestrator()
    
    test_queries = [
        "What is the revenue for Google in 2023?",
        "Show me Alphabet's net income",
        "Compare Facebook and Apple",
        "Analysis for Meta Platforms"
    ]
    
    for q in test_queries:
        normalized = orch._normalize_query_entities(q)
        print(f"Original:   '{q}'")
        print(f"Normalized: '{normalized}'")
        print("-" * 40)
        
    orch.close()

if __name__ == "__main__":
    asyncio.run(test_normalization())
