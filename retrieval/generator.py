from typing import List
from openai import OpenAI
from utils.data_models import RetrievalResult
from utils.config import Config


class Generator:
    """Generate answers using LLM based on retrieved context"""
    
    def __init__(self, openai_client: OpenAI):
        """Initialize generator with OpenAI client"""
        self.client = openai_client
    
    def build_context(self, chunks: List[RetrievalResult]) -> str:
        """
        Build context string from chunks
        
        Args:
            chunks: List of retrieval results
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for chunk in chunks:
            context_parts.append(f"[Page {chunk.page}]\n{chunk.content}\n")
        return "\n---\n".join(context_parts)
    
    def generate_answer(self, query: str, context: str) -> str:
        """
        Generate answer using LLM
        
        Args:
            query: User query
            context: Retrieved context
            
        Returns:
            Generated answer
        """
        system_prompt = """You are a technical assistant for Ford F-150 suspension systems.
Answer questions based ONLY on the provided context from the service manual.
If the context doesn't contain the answer, say so clearly.
Be precise and cite page numbers when relevant."""

        user_prompt = f"""Context from service manual:
{context}

Question: {query}

Answer:"""

        try:
            response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=Config.LLM_TEMPERATURE,
                max_tokens=Config.LLM_MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating answer: {e}"
