from retriever import SECDataRetriever
from processor import SECFilingProcessor
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_rag_pipeline():
    # 1. Initialize
    retriever = SECDataRetriever()
    processor = SECFilingProcessor()
    
    cik = "320193" # Apple
    print(f"Fetching metadata for Apple (CIK: {cik})...")
    
    try:
        # 2. Get URL
        metadata = retriever.get_latest_filing_metadata(cik)
        url = metadata['url']
        print(f"Found URL: {url}")
        
        # 3. Download HTML
        # We use requests directly here to simulate the fetching step, 
        # ensuring we pass the USER_AGENT header as required by SEC.
        headers = {
            "User-Agent": os.getenv("USER_AGENT"),
            "Host": "www.sec.gov"
        }
        print("Downloading HTML...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
        
        # 4. Clean and Extract
        print("Cleaning HTML and extracting Risk Factors...")
        clean_text = processor.clean_html(html_content)
        risk_factors = processor.extract_risk_factors(clean_text)
        
        print(f"Risk Factors Length: {len(risk_factors)} chars")
        
        if len(risk_factors) < 100 or "not found" in risk_factors:
            print("WARNING: Risk factors extraction might have failed or found TOC.")
            print(f"Preview: {risk_factors[:200]}")
        
        # 5. Chunk
        chunks = processor.chunk_text(risk_factors)
        print(f"Number of Chunks: {len(chunks)}")
        
        if chunks:
            print(f"\n--- Chunk 1 Preview ---\n{chunks[0][:500]}...")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rag_pipeline()
