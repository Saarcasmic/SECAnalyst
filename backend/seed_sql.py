import asyncio
import logging
from orchestrator import Orchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TARGET_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META']

async def seed():
    logger.info("Initializing Orchestrator for SQL Seeding...")
    orch = Orchestrator()
    
    for ticker in TARGET_TICKERS:
        logger.info(f"--- Seeding {ticker} ---")
        query = f"Analyze the Revenue, Net Income, and Total Assets for {ticker} for fiscal year 2023."
        
        try:
            logger.info(f"Running query: '{query}'")
            # Iterate (consume) the generator to trigger all tool calls
            async for chunk in orch.handle_query(query):
                pass 
            logger.info(f"Finished {ticker}.")
        except Exception as e:
            logger.error(f"Error seeding {ticker}: {e}")
            
    # Cleanup
    if hasattr(orch, 'close'):
        orch.close()
    logger.info("SQL Seeding Complete.")

if __name__ == "__main__":
    asyncio.run(seed())
