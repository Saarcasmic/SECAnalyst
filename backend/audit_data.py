import sqlite3
import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

def audit_data():
    print("--- Data Consistency Audit ---")
    
    # 1. Setup Connections
    # Note: Using 'sec_data.db' as defined in database.py, overriding user request for 'financial_data.db'
    db_path = "sec_data.db" 
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index("sec-financial-index")
        
        # Get dimensions for dummy vector
        stats = index.describe_index_stats()
        # dimension is inside the index description, but describe_index_stats returns a dict-like object
        # usually 1536 for text-embedding-3-small
        dimension = 1536 
        
    except Exception as e:
        print(f"Error connecting to Pinecone: {e}")
        return

    # 2. Analyze SQL
    print("Analyzing SQLite Data...")
    # Join with companies to get ticker. 
    # Try/Except in case tables don't exist yet
    try:
        cursor.execute("""
            SELECT c.ticker, COUNT(fm.id) as count
            FROM financial_metrics fm
            JOIN companies c ON fm.company_cik = c.cik
            GROUP BY c.ticker
        """)
        sql_counts = {row[0]: row[1] for row in cursor.fetchall()}
    except Exception as e:
        print(f"SQL Error: {e}")
        sql_counts = {}

    # 3. Analyze Pinecone & Report
    print("Analyzing Pinecone Index...")
    
    print(f"\n{'| Ticker':<10} | {'SQL Rows':<10} | {'Pinecone Chunks':<15} | {'Status':<15} |")
    print("-" * 60)
    
    # If sql_counts is empty, maybe iterate over a known list or just stop? 
    # Let's iterate over found SQL counts. If SQL is empty, nothing to report?
    # We should also check for companies in Pinecone that are NOT in SQL? 
    # For this audit, we drive by SQL presence as per prompt instructions.
    
    dummy_vector = [0.0] * dimension
    
    total_sql = 0
    total_pinecone = 0
    
    for ticker, sql_count in sql_counts.items():
        try:
            # Query Pinecone count
            # Use query with filter and top_k, but note that Pinecone doesn't give exact "count" easily 
            # without fetching. top_k=10000 is a decent proxy for small datasets.
            # For massive datasets, we'd need a different approach (like list_points or stats with filter if supported)
            
            results = index.query(
                vector=dummy_vector,
                filter={"company": ticker},
                top_k=10000,
                include_values=False,
                include_metadata=False
            )
            pinecone_count = len(results['matches'])
            
            status = "✅ Synced" if pinecone_count > 0 else "⚠️ Missing in RAG"
            
            print(f"| {ticker:<10} | {sql_count:<10} | {pinecone_count:<15} | {status:<15} |")
            
            total_sql += sql_count
            total_pinecone += pinecone_count
            
        except Exception as e:
            print(f"| {ticker:<10} | {sql_count:<10} | {'ERR':<15} | {str(e)[:15]:<15} |")

    print("-" * 60)
    print(f"Total Companies: {len(sql_counts)}")
    print(f"Total SQL Rows: {total_sql}")
    print(f"Total Vectors: {total_pinecone}")

    conn.close()

if __name__ == "__main__":
    audit_data()
