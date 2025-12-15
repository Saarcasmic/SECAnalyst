from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

class QueryClassifier:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=api_key
        )
        
        self.parser = JsonOutputParser()
        
        # Define the prompt
        template = """
        Analyze this user query: '{query}'.
        
        Your goal is to categorize the query and extract key information.
        
        Types:
        - "metric": User is asking for a specific financial number (e.g., Revenue, Income, Debt).
        - "rag": User is asking a qualitative question, looking for risks, summaries, or textual information.
        - "comparison": User is comparing two companies (Not yet implemented, but identify if so).
        
        Extract:
        - "type": One of ["metric", "rag", "comparison"]
        - "companies": List of stock tickers usually found in the query (e.g., ["AAPL", "MSFT"]). If Apple is mentioned, use AAPL.
        - "metric": The financial metric requested (e.g., "Revenues", "NetIncomeLoss"). If unsure, guess the closest XBRL tag or standard name. None if not a metric query.
        - "year": The fiscal year requested as an integer (e.g., 2023). If asking for "latest" or "recent", return 2024. If not specified, return 0.
        
        Examples:
        - "What was Apple's revenue in 2023?" -> {{"type": "metric", "companies": ["AAPL"], "metric": "Revenues", "year": 2023}}
        - "What are the risks for Apple?" -> {{"type": "rag", "companies": ["AAPL"], "metric": null, "year": 2024}}
        
        Return ONLY valid JSON.
        """
        
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["query"],
        )
        
        self.chain = self.prompt | self.llm | self.parser

    def classify(self, query: str) -> dict:
        """
        Classify the user query and return a structured dict.
        """
        try:
            return self.chain.invoke({"query": query})
        except Exception as e:
            print(f"Classification failed: {e}")
            # Fallback
            return {"type": "rag", "companies": [], "metric": None, "year": 0}

class AnalysisAgent:
    def generate_comparison_data(self, repo, companies, metric, years=None):
        """
        Generates a structured dictionary for charting.
        """
        import json
        datasets = []
        
        # Ensure we have a list of years. Default to [2021, 2022, 2023] if not provided.
        # This prevents 2025/future years which have no data yet.
        if not years:
            years = [2021, 2022, 2023]
            
        for company in companies:
            data_points = []
            for year in years:
                try:
                    # Clean up the metric string from "$" etc if needed, but repo handles this.
                    # This returns a string like "$383,285,000,000" or None
                    val_str = repo.get_metric(company, metric, year)
                    
                    if val_str is None or val_str.startswith("Data not found"):
                        data_points.append(0)
                        continue

                    # Parse string to float for charting
                    # Remove '$', ',', and whitespace
                    # Also remove the (Cached)/(Fetched) suffix
                    clean_val = val_str.split('(')[0].replace('$', '').replace(',', '').strip()
                    data_points.append(float(clean_val))
                except:
                    # If data missing or parse error, append 0
                    data_points.append(0)
            
            datasets.append({
                "name": company,
                "data": data_points
            })
            
        chart_data = {
            "type": "chart",
            "title": f"{metric} Comparison ({min(years)}-{max(years)})",
            "labels": [str(y) for y in years],
            "datasets": datasets
        }
        
        print(f"DEBUG: Generated Chart Data: {json.dumps(chart_data, indent=2)}")
        return chart_data
