"""Query rewriting with step-back prompting"""

from typing import Dict
from openai import OpenAI
from utils.data_models import QueryType
from utils.config import Config


class QueryRewriter:
    """Query rewriting with step-back prompting and decomposition"""
    
    STEP_BACK_PROMPT = """You are an expert at query rewriting for retrieval systems.

Rewrite the user's specific question into a broader "step-back" question that captures general context.

RULES:
1. Keep the same entity/person/product (NO drift)
2. Generalize the scope
3. Remove overly specific constraints
4. Keep domain anchored
5. Output should be 5-15 words

Examples:
- "What is the torque spec for the front shock absorber?" → "What are the torque specifications for suspension components?"
- "Which team did X play for in 2007?" → "What is X's career history?"

Return ONLY the rewritten query."""

    def __init__(self, openai_client: OpenAI):
        """Initialize query rewriter with OpenAI client"""
        self.client = openai_client
    
    def analyze_query(self, query: str) -> Dict:
        """
        Analyze query type and complexity
        
        Args:
            query: User query
            
        Returns:
            Dictionary with query analysis
        """
        query_lower = query.lower()
        confidence = 1.0
        
        query_type = None
        expected_chunks = Config.FACTUAL_DEFAULT
        
        if any(kw in query_lower for kw in ["summarize", "all", "complete", "overview", "list all"]):
            query_type = QueryType.SUMMARY
            expected_chunks = Config.SUMMARY_DEFAULT
            confidence = 0.9
        elif any(kw in query_lower for kw in ["how to", "steps", "procedure", "install", "remove", "replace"]):
            query_type = QueryType.PROCEDURAL
            expected_chunks = Config.PROCEDURAL_DEFAULT
            confidence = 0.9
        elif any(kw in query_lower for kw in ["compare", "vs", "versus", "difference", "between"]):
            query_type = QueryType.COMPARISON
            expected_chunks = 6
            confidence = 0.9
        elif any(kw in query_lower for kw in ["when", "date", "time", "year", "before", "after"]):
            query_type = QueryType.TEMPORAL
            expected_chunks = Config.FACTUAL_DEFAULT
            confidence = 0.8
        else:
            query_type = QueryType.FACTUAL
            expected_chunks = Config.FACTUAL_DEFAULT
            confidence = 0.7
        
        out_of_scope_keywords = ["weather", "stock", "news", "politics", "sports", "celebrity"]
        if any(kw in query_lower for kw in out_of_scope_keywords):
            query_type = QueryType.OUT_OF_SCOPE
        
        if confidence < 0.8 and query_type != QueryType.OUT_OF_SCOPE:
            try:
                llm_type, llm_chunks = self._classify_with_llm(query)
                if llm_type:
                    query_type = llm_type
                    expected_chunks = llm_chunks
            except Exception:
                pass
        
        return {
            "type": query_type,
            "expected_chunks": expected_chunks,
            "needs_rewriting": query_type in [QueryType.FACTUAL, QueryType.PROCEDURAL],
            "needs_decomposition": query_type in [QueryType.COMPARISON, QueryType.MULTI_HOP]
        }
    
    def _classify_with_llm(self, query: str) -> tuple:
        """
        Use LLM to classify query type
        
        Args:
            query: User query
            
        Returns:
            Tuple of (QueryType, expected_chunks)
        """
        classification_prompt = f"""Classify this query into one of these types:
- FACTUAL: Single fact or definition (e.g., "What is X?")
- SUMMARY: Comprehensive overview (e.g., "Summarize all X")
- PROCEDURAL: Step-by-step instructions (e.g., "How to do X?")
- COMPARISON: Comparing items (e.g., "X vs Y")
- TEMPORAL: Time-related (e.g., "When did X happen?")
- OUT_OF_SCOPE: Not about technical/automotive topics

Query: "{query}"

Respond with ONLY the type name (e.g., "FACTUAL")."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": classification_prompt}],
                temperature=0.0,
                max_tokens=20
            )
            
            result = response.choices[0].message.content.strip().upper()
            
            type_mapping = {
                "FACTUAL": (QueryType.FACTUAL, Config.FACTUAL_DEFAULT),
                "SUMMARY": (QueryType.SUMMARY, Config.SUMMARY_DEFAULT),
                "PROCEDURAL": (QueryType.PROCEDURAL, Config.PROCEDURAL_DEFAULT),
                "COMPARISON": (QueryType.COMPARISON, 6),
                "TEMPORAL": (QueryType.TEMPORAL, Config.FACTUAL_DEFAULT),
                "OUT_OF_SCOPE": (QueryType.OUT_OF_SCOPE, 0)
            }
            
            return type_mapping.get(result, (QueryType.FACTUAL, Config.FACTUAL_DEFAULT))
            
        except Exception:
            return None, None
    
    def rewrite(self, query: str, analysis: Dict) -> Dict:
        """
        Apply step-back rewriting if beneficial
        
        Args:
            query: Original query
            analysis: Query analysis result
            
        Returns:
            Dictionary with rewrite result
        """
        if analysis["type"] == QueryType.OUT_OF_SCOPE:
            return {
                "status": "rejected",
                "reason": "Query is outside the scope of this system (automotive service manual)",
                "suggestion": "Please ask about vehicle maintenance, repair procedures, or technical specifications."
            }
        
        if not analysis["needs_rewriting"]:
            return {
                "status": "success",
                "stepback_query": query,
                "use_stepback": False
            }
        
        try:
            response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[
                    {"role": "system", "content": self.STEP_BACK_PROMPT},
                    {"role": "user", "content": query}
                ],
                temperature=0.1,
                max_tokens=100
            )
            
            stepback_query = response.choices[0].message.content.strip()
            
            return {
                "status": "success",
                "stepback_query": stepback_query,
                "use_stepback": True
            }
        
        except Exception as e:
            return {
                "status": "success",
                "stepback_query": query,
                "use_stepback": False,
                "error": str(e)
            }
