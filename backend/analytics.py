import os
from dotenv import load_dotenv
from sqlalchemy import func, distinct
from database import get_db_session
from models import FinancialMetric, Company
from pinecone import Pinecone

# Load env vars
load_dotenv()

def generate_analytics():
    print("--- Analytics Report ---")
    
    # 1. SQL Metrics
    session = next(get_db_session())
    try:
        total_rows = session.query(FinancialMetric).count()
        total_companies = session.query(Company).count()
        unique_metrics = session.query(distinct(FinancialMetric.metric_name)).count()
        
        # Get list of tickers for the snippet
        companies = session.query(Company.ticker).all()
        company_list = [c[0] for c in companies]
        
    finally:
        session.close()

    # 2. Pinecone Metrics
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index("sec-financial-index")
        stats = index.describe_index_stats()
        total_vectors = stats.total_vector_count
        
        # Estimate pages: 1 vector roughly equals a chunk of text. 
        # If we assume 1 chunk ~ 1000 chars and 1 page ~ 3000 chars.
        # This is very rough but serves the resume purpose.
        # Actual estimation: total_vectors * (chunk_size / page_size)
        estimated_pages = int(total_vectors / 3) 
    except Exception as e:
        print(f"Error connecting to Pinecone: {e}")
        total_vectors = 0
        estimated_pages = 0

    # 3. Output Resume Snippet
    print("\n[RESUME SNIPPET]")
    print(f"Engineered a financial intelligence system indexing {total_vectors:,} vectors and {total_rows:,} structured data points across {total_companies} major tech equities.")
    print(f"Achieved comprehensive coverage of {unique_metrics:,} distinct GAAP financial metrics.")

    print("\n[DETAILED STATS]")
    print(f"Total Companies: {total_companies} ({', '.join(company_list[:5])}{'...' if len(company_list) > 5 else ''})")
    print(f"Total Structured Rows: {total_rows:,}")
    print(f"Unique Metrics: {unique_metrics:,}")
    print(f"Total Vectors: {total_vectors:,}")
    print(f"Estimated Pages Processed: {estimated_pages:,}")

if __name__ == "__main__":
    generate_analytics()
