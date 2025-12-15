from retriever import SECDataRetriever

def debug():
    r = SECDataRetriever()
    cik = "320193" # AAPL
    try:
        meta = r.get_latest_filing_metadata(cik, "10-K")
        print("--- Metadata ---")
        print(f"Accession: {meta['accessionNumber']}")
        print(f"Primary Doc: {meta['primaryDocument']}")
        print(f"Generated URL: {meta['url']}")
        
        # Check standard folder URL too
        # standard is /data/cik/acc_num_no_dash/index.json
        print(f"Index URL: {meta['url'].rsplit('/', 1)[0]}/index.json")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug()
