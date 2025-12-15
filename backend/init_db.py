import logging
from database import engine, Base, SessionLocal
from models import Company, FinancialMetric 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Creates tables and seeds initial company data.
    """
    # 1. Create Tables
    logger.info("Creating tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully.")

    # 2. Seed Companies
    session = SessionLocal()
    try:
        # Standard list of tech giants to track
        companies = [
            {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology", "cik": "0000320193"},
            {"ticker": "MSFT", "name": "Microsoft Corp", "sector": "Technology", "cik": "0000789019"},
            {"ticker": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "cik": "0001652044"},
            {"ticker": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "cik": "0001018724"},
            {"ticker": "NVDA", "name": "NVIDIA Corp", "sector": "Technology", "cik": "0001045810"},
            {"ticker": "TSLA", "name": "Tesla Inc.", "sector": "Automotive", "cik": "0001318605"},
            {"ticker": "META", "name": "Meta Platforms Inc.", "sector": "Technology", "cik": "0001326801"},
        ]

        for company_data in companies:
            # Check if company exists
            exists = session.query(Company).filter_by(ticker=company_data['ticker']).first()
            if not exists:
                company = Company(**company_data)
                session.add(company)
                logger.info(f"Added company: {company_data['ticker']}")
            else:
                logger.info(f"Skipping {company_data['ticker']} (already exists)")

        session.commit()
        logger.info("Database seeding complete.")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    print("⚠️  Initializing Database...")
    init_db()
    print("✅  Done!")