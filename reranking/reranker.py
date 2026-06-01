from typing import List
from utils.data_models import RetrievalResult

try:
    import cohere
    COHERE_AVAILABLE = True
except ImportError:
    COHERE_AVAILABLE = False


class Reranker:
    """Cohere reranking for improved precision"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize reranker
        
        Args:
            api_key: Cohere API key
        """
        self.cohere_client = None
        if COHERE_AVAILABLE and api_key:
            self.cohere_client = cohere.Client(api_key)
    
    def rerank(self, query: str, results: List[RetrievalResult], top_k: int = 50) -> List[RetrievalResult]:
        """
        Rerank results using Cohere
        
        Args:
            query: Search query
            results: Initial retrieval results
            top_k: Number of results to return
            
        Returns:
            Reranked results
        """
        if not self.cohere_client or not results:
            return results[:top_k]
        
        try:
            documents = [r.content for r in results]
            
            rerank_response = self.cohere_client.rerank(
                model="rerank-english-v3.0",
                query=query,
                documents=documents,
                top_n=min(top_k, len(results)),
                return_documents=False
            )
            
            reranked = []
            for idx, result in enumerate(rerank_response.results, 1):
                original = results[result.index]
                reranked.append(RetrievalResult(
                    chunk_id=original.chunk_id,
                    content=original.content,
                    score=result.relevance_score,
                    page=original.page,
                    rank=idx
                ))
            
            return reranked
        
        except Exception as e:
            print(f"⚠️  Reranking failed: {e}")
            return results[:top_k]
