import os
import glob
import logging
import asyncio
from dotenv import load_dotenv
from sec_edgar_downloader import Downloader
from processor import SECFilingProcessor
from vector_store import VectorDB

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of companies to ingest
TARGET_COMPANIES = {
    "GOOGL": "1652044",
    "AMZN": "1018724",
    "MSFT": "789019",
    "NVDA": "1045810",
    "TSLA": "1318605",
    "AAPL": "320193"
}

# Directory to save filings
DOWNLOAD_DIR = "sec_filings"

async def ingest_company(ticker: str, cik: str):
    processor = SECFilingProcessor()
    vector_db = VectorDB()
    
    # Initialize Downloader
    # email is required, getting from env or default
    user_agent_str = os.getenv("USER_AGENT", "Saar agrawalsaar16@gmail.com")
    try:
        # Extract company name and email roughly from user agent string "Name Email"
        # sec_edgar_downloader params: (company_name, email_address, download_folder)
        parts = user_agent_str.split(" ")
        company_name = parts[0]
        email = parts[-1] 
        dl = Downloader(company_name, email, DOWNLOAD_DIR)
    except Exception as e:
        logger.error(f"Error initializing downloader: {e}")
        return

    try:
        logger.info(f"--- Processing {ticker} (CIK: {cik}) ---")
        
        # 1. Download Latest 10-K
        logger.info(f"Downloading 10-K for {ticker}...")
        # limit=1 gets the latest
        num_downloaded = dl.get("10-K", ticker, limit=1)
        
        if num_downloaded == 0:
            logger.warning(f"No 10-K found for {ticker}")
            return
            
        # 2. Find the downloaded file
        # Pattern: sec_filings/sec-edgar-filings/{ticker}/10-K/{accession_number}/primary-document.html
        # or .txt depending on what it downloads. It usually downloads full text.
        # Let's glob for it.
        search_path = os.path.join(DOWNLOAD_DIR, "sec-edgar-filings", ticker, "10-K", "*", "*.txt")
        # sec-edgar-downloader downloads the full text submission as .txt usually (or .html if specified, default is usually .txt which includes HTML)
        files = glob.glob(search_path)
        if not files:
             # Try .html or .htm
             search_path = os.path.join(DOWNLOAD_DIR, "sec-edgar-filings", ticker, "10-K", "*", "*.htm*")
             files = glob.glob(search_path)
        
        if not files:
            logger.error(f"Downloaded file not found on disk for {ticker}")
            return
            
        # Take the first one found (latest)
        file_path = files[0]
        logger.info(f"Reading file: {file_path}")
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
        
        # 3. Clean & Extract
        logger.info("Cleaning HTML...")
        clean_text = processor.clean_html(raw_text)
        
        logger.info("Extracting Risk Factors...")
        risk_text = processor.extract_risk_factors(clean_text)
        
        # Fallback Check
        if not risk_text or len(risk_text) < 2000:
            logger.warning(f"Risk factor extraction failed or too short ({len(risk_text) if risk_text else 0} chars) for {ticker}. Falling back to FULL TEXT ingestion.")
            risk_text = clean_text  # Use the whole document

        # 4. Chunk
        chunks = processor.chunk_text(risk_text)
        logger.info(f"Generated {len(chunks)} text chunks.")
        
        # 5. Upsert to Pinecone
        # We can extract year from file path or just use current year "2023" as placeholder for "latest"
        year = "2023" 
        
        meta_base = {
            "company": ticker,
            "year": year,
            "source": "10-K"
        }
        
        vector_db.upsert_chunks(chunks, meta_base)
        logger.info(f"Successfully indexed {ticker}!")

    except Exception as e:
        logger.error(f"Failed to ingest {ticker}: {e}")

async def main():
    logger.info("Starting Batch Ingestion...")
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        
    for ticker, cik in TARGET_COMPANIES.items():
        await ingest_company(ticker, cik)
    logger.info("Batch Ingestion Complete.")

if __name__ == "__main__":
    asyncio.run(main())
