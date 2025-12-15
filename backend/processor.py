from bs4 import BeautifulSoup
import re
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

# Alias dictionary for text-based metric extraction
METRIC_ALIASES = {
    "Revenue": [
        "Total Revenues", "Revenues", "Net Revenues", "Total Net Revenues",
        "Net Sales", "Total Net Sales", "Revenue", "Total Revenue"
    ],
    "Net Income": [
        "Net Income", "Net Earnings", "Net Loss", "Net Profit",
        "Net income (loss)", "Net income"
    ],
    "Total Assets": [
        "Total Assets", "Assets", "Total assets"
    ],
    "Gross Profit": [
        "Gross Profit", "Gross profit"
    ],
    "Operating Income": [
        "Operating Income", "Operating income", "Income from operations"
    ]
}

class SECFilingProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        # Initialize LLM for smart extraction fallback
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def clean_html(self, html_content: str) -> str:
        """
        Clean HTML content by removing scripts, styles, and tables,
        and extracting text.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Replace <br> tags with newlines to preserve some structure
        for br in soup.find_all("br"):
            br.replace_with("\n")
            
        # Get text with separator to avoid merging words
        text = soup.get_text(separator=" ", strip=True)
        return text

    def extract_risk_factors(self, text: str) -> str:
        """
        Extract the 'Item 1A. Risk Factors' section using Regex.
        """
        pattern = re.compile(
            r'(?i)(?:Item\s+1A[\.\\s]*Risk\s+Factors)(.*?)(?:Item\s+(?:1B|2)[\.\\s])',
            re.DOTALL
        )
        
        matches = pattern.findall(text)
        
        if not matches:
             return "Risk Factors section not found."
             
        longest_match = max(matches, key=len)
        return longest_match.strip()

    def chunk_text(self, text: str) -> list:
        """
        Chunk the text using LangChain's RecursiveCharacterTextSplitter.
        """
        return self.text_splitter.split_text(text)

    def _find_financial_statements_chunk(self, text: str) -> str:
        """
        Find the chunk of text that likely contains financial statements.
        Searches for keywords like 'Consolidated Statement of Operations' or 'Item 8'.
        """
        keywords = [
            "Consolidated Statements of Operations",
            "Consolidated Statement of Operations", 
            "Statement of Operations",
            "Statements of Income",
            "Item 8",
            "FINANCIAL STATEMENTS"
        ]
        
        for keyword in keywords:
            idx = text.lower().find(keyword.lower())
            if idx != -1:
                # Return a 5000 character chunk around the keyword
                start = max(0, idx - 500)
                end = min(len(text), idx + 4500)
                return text[start:end]
        
        # Fallback: return first 5000 chars if no keyword found
        return text[:5000]

    def extract_metric_via_llm(self, text_chunk: str, metric_name: str, year: str) -> str:
        """
        Use GPT-4o-mini to extract a financial metric from a text chunk.
        
        Args:
            text_chunk: The part of the 10-K containing financial tables.
            metric_name: The metric to extract (e.g., "Revenue").
            year: The fiscal year (e.g., "2023").
        
        Returns:
            The extracted value or "None".
        """
        prompt = f"""Context: The following is text from a company's 10-K financial filing.
Task: Extract the value for '{metric_name}' for the fiscal year '{year}'.

Rules:
1. Look for the 'Consolidated Statement of Operations' or 'Income Statement'.
2. Find the row corresponding to {metric_name} (it might be called 'Net Sales', 'Revenues', 'Total Revenue', etc.).
3. Return ONLY the raw number (e.g., '307394' or '307,394'). Do not include words like 'million'.
4. If not found, return 'None'.

Text:
{text_chunk[:4000]}...
"""
        try:
            response = self.llm.invoke(prompt)
            result = response.content.strip()
            
            # Clean up the result
            if result.lower() == "none" or not result:
                return None
            
            # Remove any non-numeric characters except commas and periods
            clean_result = re.sub(r'[^\d,.]', '', result)
            if clean_result:
                return f"${clean_result}"
            return None
            
        except Exception as e:
            print(f"LLM extraction error: {e}")
            return None

    def extract_financial_metric(self, text: str, metric_name: str, year: str = None) -> str:
        """
        Extract a financial metric value from raw text.
        
        Strategy:
        1. Try fast regex patterns first.
        2. If regex fails, use LLM-based extraction as smart fallback.
        
        Args:
            text: The raw/cleaned text from a 10-K filing.
            metric_name: The standardized metric name (e.g., "Revenue").
            year: Optional year to help narrow down the search.
        
        Returns:
            The found value (e.g., "$307,394") or "Data not found".
        """
        # Get aliases for the metric
        aliases = METRIC_ALIASES.get(metric_name, [metric_name])
        
        # STEP 1: Fast Regex Path
        # Google-specific hack: Look for "Revenues $ 307,394" pattern first
        if metric_name in ["Revenue", "Revenues"]:
            google_pattern = re.compile(
                r'(?i)Revenues\s+\$\s?([\d,]+)',
                re.IGNORECASE
            )
            match = google_pattern.search(text)
            if match:
                return f"${match.group(1)}"
        
        # General extraction: For each alias, look for the pattern
        for alias in aliases:
            pattern = re.compile(
                rf'(?i){re.escape(alias)}\s*[\.\:\s]*\$?\s*([\(\)?\d,]+(?:\.\d+)?)',
                re.IGNORECASE
            )
            match = pattern.search(text)
            if match:
                value = match.group(1)
                if value and value.strip():
                    clean_val = value.replace("(", "-").replace(")", "").strip()
                    return f"${clean_val}"
        
        # Fallback regex: Search for the alias and grab the next number
        for alias in aliases:
            idx = text.lower().find(alias.lower())
            if idx != -1:
                snippet = text[idx:idx + 100]
                num_pattern = re.compile(r'\$?\s*([\d,]+(?:\.\d+)?)')
                num_match = num_pattern.search(snippet[len(alias):])
                if num_match:
                    return f"${num_match.group(1)}"
        
        # STEP 2: Smart LLM Fallback
        if year:
            financial_chunk = self._find_financial_statements_chunk(text)
            llm_result = self.extract_metric_via_llm(financial_chunk, metric_name, year)
            if llm_result:
                return llm_result
        
        return "Data not found"
