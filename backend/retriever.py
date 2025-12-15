import os
import requests
from dotenv import load_dotenv
from utils import RateLimiter

load_dotenv()

class SECDataRetriever:
    def __init__(self):
        self.user_agent = os.getenv("USER_AGENT")
        if not self.user_agent:
            raise ValueError("USER_AGENT not found in environment variables. Please check your .env file.")
        
        # SEC API strictly requires a User-Agent header
        self.headers = {
            "User-Agent": self.user_agent,
            "Accept-Encoding": "gzip, deflate",
            "Host": "data.sec.gov"
        }

    # Apply RateLimiter: 10 calls per 1 second
    @RateLimiter(max_calls=10, period=1.0)
    def _make_request(self, url: str) -> dict:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 429:
                raise Exception("Rate limit hit (429). Please slow down.")
            
            if response.status_code == 404:
                # 404 might mean invalid CIK or simply no data
                return None
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise

    def get_company_facts(self, cik: str) -> dict:
        """
        Fetch company facts for a given CIK.
        Validates and pads CIK to 10 digits.
        """
        # Pad CIK to 10 digits (e.g., 320193 -> 0000320193)
        padded_cik = cik.zfill(10)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{padded_cik}.json"
        
        data = self._make_request(url)
        if data is None:
            raise ValueError(f"No data found for CIK: {cik}")
            
        return data

    def get_submissions(self, cik: str) -> dict:
        """
        Fetch submissions history for a given CIK.
        """
        padded_cik = cik.zfill(10)
        url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"
        
        data = self._make_request(url)
        if data is None:
            raise ValueError(f"No data found for CIK: {cik}")
        
        return data

    def get_latest_filing_metadata(self, cik: str, form_type: str = "10-K") -> dict:
        """
        Fetch metadata and construct URL for the latest filing of a specific type.
        """
        data = self.get_submissions(cik)
        recent = data.get('filings', {}).get('recent', {})
        
        if not recent:
            raise ValueError(f"No recent filings found for CIK: {cik}")
            
        forms = recent.get('form', [])
        accession_numbers = recent.get('accessionNumber', [])
        primary_documents = recent.get('primaryDocument', [])
        
        for i, form in enumerate(forms):
            if form == form_type:
                acc_num = accession_numbers[i]
                primary_doc = primary_documents[i]
                
                # Construct URL
                # URL format: https://www.sec.gov/Archives/edgar/data/{cik}/{acc_num_no_dashes}/{primary_doc}
                acc_num_no_dashes = acc_num.replace("-", "")
                cik_stripped = str(int(cik)) # Remove leading zeros for URL construction usually? 
                # Actually, SEC URLs often use the CIK without leading zeros or with? 
                # Let's check standard EDGAR URLs. usually /data/320193/ not /data/0000320193/
                # I will try to use the stripped CIK for the URL path as is common practice.
                
                url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_num_no_dashes}/{primary_doc}"
                
                return {
                    "accessionNumber": acc_num,
                    "primaryDocument": primary_doc,
                    "url": url,
                    "filingDate": recent.get('filingDate', [])[i]
                }
                
        raise ValueError(f"No filing of type {form_type} found for CIK: {cik}")

