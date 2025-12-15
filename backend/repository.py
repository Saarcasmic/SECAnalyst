from sqlalchemy.orm import Session
from models import Company, FinancialMetric
from retriever import SECDataRetriever

# Helper mapping for Phase 2
TICKER_TO_CIK = {
    'AAPL': '320193',
    'MSFT': '789019',
    'GOOGL': '1652044',
    'AMZN': '1018724',
    'NVDA': '1045810',
    'TSLA': '1318605',
    'META': '1326801'
}

# Comprehensive alias dictionary for different companies' XBRL tags
METRIC_ALIASES = {
    "Revenue": [
        "Revenues", "Revenue", "TotalRevenue", "TotalRevenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet", "SalesRevenueGoodsNet", "NetRevenues",
        "TotalNetRevenues", "NetSales", "TotalNetSales"
    ],
    "Net Income": [
        "NetIncomeLoss", "NetIncome", "NetEarnings", 
        "ProfitLoss", "NetIncomeLossAttributableToParent"
    ],
    "Total Assets": [
        "Assets", "TotalAssets"
    ],
    "Gross Profit": [
        "GrossProfit", "GrossProfitLoss"
    ],
    "Operating Income": [
        "OperatingIncomeLoss", "OperatingIncome"
    ],
    "EPS": [
        "EarningsPerShareBasic", "EarningsPerShareDiluted"
    ]
}

class FinancialDataRepository:
    def __init__(self, db_session: Session, sec_retriever: SECDataRetriever):
        self.db = db_session
        self.retriever = sec_retriever

    def get_metric(self, ticker: str, metric_name: str, year: int) -> str:
        """
        Get a financial metric for a specific year.
        Checks DB first. If missing, fetches from SEC API, saves to DB, then returns.
        """
        # 1. Resolve Ticker to CIK
        cik = TICKER_TO_CIK.get(ticker.upper())
        if not cik:
            raise ValueError(f"Ticker {ticker} not found in supported list.")
        
        padded_cik = cik.zfill(10)

        # Normalize metric name (Handle plural "Revenues" -> "Revenue")
        # This fixes the issue where "Revenues" wouldn't find the alias list for "Revenue"
        canonical_name = metric_name
        if metric_name in ["Revenues", "Total Revenues", "Net Revenue", "Net Revenues"]:
            canonical_name = "Revenue"
        elif metric_name in ["Net Income", "Net Earnings", "Net Loss"]:
            canonical_name = "Net Income"
            
        print(f"DEBUG: Request for '{metric_name}' normalized to '{canonical_name}'")

        # 2. Check Database
        # First ensure company exists in DB
        company = self.db.query(Company).filter(Company.cik == padded_cik).first()
        if not company:
            # We don't have company details yet, but we will fetch them if we go to network
            pass
        
        # Check for metric (check both original and canonical to be safe, or just canonical if we save as canonical)
        # We'll check canonical for DB persistence to avoid duplicates
        metric = self.db.query(FinancialMetric).filter(
            FinancialMetric.company_cik == padded_cik,
            FinancialMetric.metric_name == canonical_name,
            FinancialMetric.fiscal_year == year,
            FinancialMetric.fiscal_period == 'FY' # For now, assume we want full year
        ).first()

        if metric:
            return f"${metric.value:,.0f} (Cached)"

        # 3. Fetch from API if not in DB
        print(f"DEBUG: Cache miss for {ticker} {canonical_name} {year}. Fetching from API...")
        
        # Ensure company is in DB before adding metrics
        if not company:
            # For this phase, we'll just create it with available info
            # In a real app, we'd fetch company metadata
            company = Company(cik=padded_cik, ticker=ticker.upper(), name=f"{ticker} Inc.") 
            self.db.add(company)
            self.db.commit()

        # Fetch facts
        facts = self.retriever.get_company_facts(cik)
        
        # Parse logic with robust alias matching
        us_gaap = facts.get('facts', {}).get('us-gaap', {})
        
        # Get aliases for the requested metric (case-insensitive lookup)
        # Use canonical name for lookup
        metric_keys = METRIC_ALIASES.get(canonical_name, [canonical_name])
        
        # Also try direct match of original if not in aliases (fallback)
        if metric_name not in metric_keys and metric_name != canonical_name:
            metric_keys = [metric_name] + metric_keys
        
        target_val = None
        target_form = None
        target_end_date = None

        for key in metric_keys:
            if key in us_gaap:
                units = us_gaap[key].get('units', {}).get('USD', [])
                
                # Sort by end date descending to get most recent first
                sorted_units = sorted([u for u in units if 'end' in u], key=lambda x: x['end'], reverse=True)
                
                for u in sorted_units:
                    # Match criteria:
                    # 1. Form is 10-K (annual filing)
                    # 2. Either fy matches the requested year OR end date year matches
                    end_date = u.get('end', '')
                    end_year = int(end_date[:4]) if end_date else 0
                    fy = u.get('fy', 0)
                    form = u.get('form', '')
                    
                    # For 10-K filings, check both fy field AND end date year
                    if form == '10-K':
                        if fy == year or end_year == year:
                            target_val = u['val']
                            target_form = form
                            target_end_date = end_date
                            print(f"DEBUG: Found {key} for {year}: val={target_val}, end={target_end_date}, fy={fy}")
                            break
                
                if target_val is not None:
                    break
        
        if target_val is None:
             return f"Data not found for {year}"

        # 4. Save to Database
        new_metric = FinancialMetric(
            company_cik=padded_cik,
            metric_name=metric_name,
            value=target_val,
            fiscal_year=year,
            fiscal_period='FY',
            form_type=target_form
        )
        self.db.add(new_metric)
        self.db.commit()
        
        return f"${target_val:,.0f} (Fetched)"
