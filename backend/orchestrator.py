from agents import QueryClassifier, AnalysisAgent
from repository import FinancialDataRepository
from vector_store import VectorDB
from retriever import SECDataRetriever
from database import get_db_session
from database import get_db_session
from langchain_openai import ChatOpenAI
from guardrail import InputGuardrail
import os
import re

# Entity Alias Mapping
ENTITY_ALIASES = {
    "Google": "GOOGL",
    "Alphabet": "GOOGL",
    "Facebook": "META",
    "Meta Platforms": "META",
    "Amazon": "AMZN",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Tesla": "TSLA"
}

class Orchestrator:
    def __init__(self, api_key: str):
        self.classifier = QueryClassifier(api_key=api_key)
        self.analysis_agent = AnalysisAgent()
        self.guardrail = InputGuardrail(api_key=api_key)
        
        # Initialize Repo
        # Note: In a real app we'd manage the session lifecycle better (e.g. dependency injection)
        self.db_session = next(get_db_session())
        self.retriever = SECDataRetriever()
        self.repo = FinancialDataRepository(self.db_session, self.retriever)
        
        self.vector_db = VectorDB(api_key=api_key)
        
        # Summary LLM for RAG
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=api_key
        )

    def _normalize_query_entities(self, query: str) -> str:
        """
        Replace colloquial company names with valid tickers.
        """
        normalized_query = query
        for alias, ticker in ENTITY_ALIASES.items():
            # Case insensitive replacement
            pattern = re.compile(re.escape(alias), re.IGNORECASE)
            normalized_query = pattern.sub(ticker, normalized_query)
        return normalized_query

    async def handle_query(self, user_query: str):
        """
        Async generator for user queries. Yields log events and the final result.
        """
        import json
        import asyncio
        import re

        # 1. Normalize Query Entities (Google -> GOOGL, etc.)
        # This helps the classifier and any downstream logic that expects tickers or specific names
        normalized_query = self._normalize_query_entities(user_query)
        if normalized_query != user_query:
            yield json.dumps({"type": "log", "message": f"Normalizing entities: '{user_query}' -> '{normalized_query}'"}) + "\n\n"
        
        # 2. Classify (using Normalized Query)
        # Note: We still pass original query to guardrail? No, usually normalized is better if it resolves ambiguity.
        # But guardrail checks for off-topic which might be subtle. Let's pass original to guardrail to be safe?
        # Actually, let's pass normalized to everything for consistency.
        
        yield json.dumps({"type": "log", "message": f"Analyzing query: '{normalized_query}'..."}) + "\n\n"
        
        # Guardrail Check
        yield json.dumps({"type": "log", "message": "Guardrail: Checking query relevance..."}) + "\n\n"
        try:
            safety_result = await self.guardrail.check_safety(normalized_query)
            if not safety_result['allowed']:
                yield json.dumps({"type": "log", "message": f"Guardrail Blocked: {safety_result.get('reason', 'Off-topic')}"}) + "\n\n"
                yield json.dumps({"type": "result", "data": f"I cannot answer that. {safety_result.get('reason', 'It is off-topic')}. I specialize in financial analysis."}) + "\n\n"
                return
        except Exception as e:
            # If guardrail fails, log it but maybe proceed with caution or fail open/closed?
            # Creating a fail-open behavior for now to avoid blocking valid queries on error
            yield json.dumps({"type": "log", "message": f"Guardrail warning: {e}"}) + "\n\n"

        await asyncio.sleep(0.1)  # Tiny yield to ensure FLUSH

        try:
            intent = self.classifier.classify(normalized_query)
            yield json.dumps({"type": "log", "message": f"Intent detected: {intent.get('type')}"}) + "\n\n"
            
            q_type = intent.get("type")
            companies = intent.get("companies", [])
            metric = intent.get("metric")
            year = intent.get("year", 2024)
            
            # 3. Route
            if q_type == "metric":
                if not companies or not metric:
                    yield json.dumps({"type": "result", "data": "I couldn't identify the company or metric. Please try again."}) + "\n\n"
                    return
                
                ticker = companies[0]
                yield json.dumps({"type": "log", "message": f"Checking database for {ticker} {metric} ({year})..."}) + "\n\n"
                
                # Simulate a small delay for "thinking" feel if it's too fast, or just proceed
                await asyncio.sleep(0.2)
                
                try:
                    # Note: synchronous call wrapped in async def works, but blocks the loop. 
                    # For full async we'd need run_in_executor, but this is fine for now.
                    result = self.repo.get_metric(ticker, metric, year)
                    
                    if result and "cached" in str(result).lower():
                         yield json.dumps({"type": "log", "message": "Data found in cache."}) + "\n\n"
                    else:
                         yield json.dumps({"type": "log", "message": "Fetching from SEC EDGAR API..."}) + "\n\n"

                    yield json.dumps({"type": "result", "data": f"{result}"}) + "\n\n"
                except Exception as e:
                    yield json.dumps({"type": "result", "data": f"Error fetching metric: {str(e)}"}) + "\n\n"

            elif q_type == "rag":
                yield json.dumps({"type": "log", "message": "Searching knowledge base (Vector DB)..."}) + "\n\n"
                await asyncio.sleep(0.2)
                
                # Search Vector DB
                chunks = self.vector_db.query_vectors(normalized_query, top_k=3)
                
                if not chunks:
                    yield json.dumps({"type": "result", "data": "I couldn't find any relevant documents."}) + "\n\n"
                    return
                
                yield json.dumps({"type": "log", "message": f"Found {len(chunks)} relevant text chunks."}) + "\n\n"
                
                # Summarize with LLM
                yield json.dumps({"type": "log", "message": "Synthesizing answer with GPT-4o..."}) + "\n\n"
                
                context = "\n\n".join(chunks)
                prompt = f"""
                You are a financial analyst helper. Use the following context to answer the user's question.
                
                Context:
                {context}
                
                Question: {normalized_query}
                
                Answer concisely based ONLY on the context provided.
                Format your answer in clean Markdown:
                - Use bullet points for lists.
                - Use **bold** for key numbers or terms.
                - Keep paragraphs short.
                """
                
                response = self.llm.invoke(prompt)
                yield json.dumps({"type": "result", "data": f"{response.content}"}) + "\n\n"

            elif q_type == "comparison":
                if not companies:
                     yield json.dumps({"type": "result", "data": "Please specify which companies to compare."}) + "\n\n"
                     return
                
                yield json.dumps({"type": "log", "message": f"Generating {metric} comparison for {', '.join(companies)}..."}) + "\n\n"
                await asyncio.sleep(0.2)
                
                target_years = [year-2, year-1, year] if year and year > 0 else []
                
                # This returns the chart JSON directly
                chart_data = self.analysis_agent.generate_comparison_data(
                    self.repo, 
                    companies, 
                    metric, 
                    target_years
                )
                
                yield json.dumps({"type": "log", "message": "Chart data generated."}) + "\n\n"
                yield json.dumps({"type": "result", "data": chart_data}) + "\n\n"
                
            else:
                yield json.dumps({"type": "result", "data": "I'm not sure how to handle that request."}) + "\n\n"
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield json.dumps({"type": "result", "data": f"An error occurred: {str(e)}"}) + "\n\n"
            
    def close(self):
        self.db_session.close()
