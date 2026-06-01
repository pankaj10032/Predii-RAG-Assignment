"""Answer quality evaluation"""

from openai import OpenAI
from .config import Config


class Evaluator:
    """Evaluate answer quality and faithfulness"""
    
    def __init__(self, openai_client: OpenAI):
        """Initialize evaluator with OpenAI client"""
        self.client = openai_client
    
    def evaluate_faithfulness(self, answer: str, context: str) -> float:
        """
        Check if answer is supported by context
        
        Args:
            answer: Generated answer
            context: Source context
            
        Returns:
            Faithfulness score from 0.0 to 1.0
        """
        prompt = f"""Evaluate if the answer is faithful to the context.

Context:
{context[:2000]}

Answer:
{answer}

Return a score from 0.0 (unfaithful) to 1.0 (perfectly faithful).
Output only the numeric score."""

        try:
            response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=10
            )
            return float(response.choices[0].message.content.strip())
        except:
            return 0.0
