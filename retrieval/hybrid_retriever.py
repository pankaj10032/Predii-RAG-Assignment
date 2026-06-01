"""Hybrid retrieval combining dense and sparse search"""

from typing import List, Dict
from rank_bm25 import BM25Okapi
from utils.data_models import RetrievalResult


class HybridRetriever:
    """Dense (vector) + Sparse (BM25) retrieval with RRF fusion"""
    
    def __init__(self, chroma_collection, chunks_data: List[Dict]):
        """
        Initialize hybrid retriever
        
        Args:
            chroma_collection: ChromaDB collection
            chunks_data: List or dict of chunk data
        """
        self.chroma = chroma_collection
        
        if isinstance(chunks_data, list):
            self.chunks_data = {f"chunk_{c['chunk_id']:03d}": c for c in chunks_data}
        else:
            self.chunks_data = chunks_data
        
        self.chunk_ids = list(self.chunks_data.keys())
        corpus = [c['content'].lower().split() for c in self.chunks_data.values()]
        self.bm25 = BM25Okapi(corpus)
    
    def retrieve(self, query: str, top_k: int = 100) -> List[RetrievalResult]:
        """
        Hybrid retrieval with RRF fusion
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of retrieval results
        """
        dense_results = self.chroma.query(
            query_texts=[query],
            n_results=min(top_k, len(self.chunk_ids))
        )
        
        dense_scores = {}
        for doc_id, distance in zip(dense_results['ids'][0], dense_results['distances'][0]):
            dense_scores[doc_id] = 1 - distance
        
        query_tokens = query.lower().split()
        bm25_scores = self.bm25.get_scores(query_tokens)
        sparse_scores = dict(zip(self.chunk_ids, bm25_scores))
        
        k = 60
        fused_scores = {}
        
        for rank, (doc_id, _) in enumerate(sorted(dense_scores.items(), key=lambda x: x[1], reverse=True), 1):
            fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank)
        
        for rank, (doc_id, _) in enumerate(sorted(sparse_scores.items(), key=lambda x: x[1], reverse=True), 1):
            fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank)
        
        final_ranked = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for rank, (chunk_id, score) in enumerate(final_ranked, 1):
            if isinstance(chunk_id, int):
                chunk_key = f"chunk_{chunk_id:03d}"
            elif isinstance(chunk_id, str):
                if chunk_id.startswith("chunk_"):
                    chunk_key = chunk_id
                else:
                    chunk_key = f"chunk_{chunk_id}"
            else:
                continue
            
            chunk_data = self.chunks_data.get(chunk_key)
            if chunk_data:
                results.append(RetrievalResult(
                    chunk_id=str(chunk_id),
                    content=chunk_data['content'],
                    score=score,
                    page=chunk_data.get('page', 0),  # Page is at top level, not in metadata
                    rank=rank
                ))
        
        return results
