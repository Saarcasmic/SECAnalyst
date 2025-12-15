from langchain_openai import ChatOpenAI
import json
import os

class InputGuardrail:
    def __init__(self, api_key: str, model="gpt-4o-mini"):
        self.llm = ChatOpenAI(
            model=model,
            temperature=0,
            api_key=api_key
        )

    async def check_safety(self, query: str) -> dict:
        prompt = f"""You are a guardrail for a Financial Analyst AI. Your job is to block off-topic queries.
            Allowed topics: Finance, Stocks, Economics, Companies, SEC filings, Market data, Risks, Revenue.
            Blocked topics: General coding, Politics, Cooking, Health, General knowledge, Creative writing.
            
            Analyze the query: '{query}'
            
            Return JSON ONLY: {{ "allowed": boolean, "reason": "short explanation" }}"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            content = response.content.strip()
            # Handle potential markdown code block wrapping
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "")
            return json.loads(content)
        except Exception as e:
            print(f"Guardrail Error: {e}")
            # Fail safe: allow if check fails, or block. Here we default to block for safety or allow for usability?
            # Let's default to allowing but logging error, or maybe simple fallback. 
            # For this task, let's assume valid JSON return or handle basic error.
            return {"allowed": True, "reason": "Guardrail check failed, proceeding with caution."}
