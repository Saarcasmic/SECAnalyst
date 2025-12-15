from retriever import SECDataRetriever
from processor import SECFilingProcessor
from vector_store import VectorDB
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def run_ingestion():
    # Configuration
    CIK = "320193" # Apple
    TICKER = "AAPL"
    YEAR = "2024" # Targeting the latest filing which might be 2024 or 2025 FY end
    
    try:
        # 1. Initialize Components
        print("Initializing components...")
        retriever = SECDataRetriever()
        processor = SECFilingProcessor()
        # Initialize VectorDB last to ensure API keys are ready
        vector_db = VectorDB() 
        
        # 2. Get Metadata & URL
        print(f"Fetching metadata for {TICKER} (CIK: {CIK})...")
        metadata = retriever.get_latest_filing_metadata(CIK)
        url = metadata['url']
        filing_date = metadata['filingDate']
        print(f"Found URL: {url} (Filing Date: {filing_date})")
        
        # 3. Download HTML
        print("Downloading filing...")
        headers = {"User-Agent": os.getenv("USER_AGENT")}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # 4. Process Content
        print("Processing content...")
        clean_text = processor.clean_html(response.text)
        risk_factors = processor.extract_risk_factors(clean_text)
        
        if not risk_factors or len(risk_factors) < 500:
            print("WARNING: Extracted risk factors seem too short. Aborting ingestion.")
            return

        chunks = processor.chunk_text(risk_factors)
        print(f"Generated {len(chunks)} chunks.")
        
        # 5. Upsert to Vector Store
        metadata_base = {
            "company": TICKER,
            "cik": CIK,
            "year": YEAR, # Ideally derived from filing_date
            "filing_date": filing_date,
            "section": "Risk Factors"
        }
        
        vector_db.upsert_chunks(chunks, metadata_base)
        
        print("\n--- Ingestion Summary ---")
        print(f"Company: {TICKER}")
        print(f"Vectors Uploaded: {len(chunks)}")
        print("Status: Success")
        
    except Exception as e:
        print(f"Ingestion failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_ingestion()
