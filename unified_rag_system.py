"""Unified RAG System - Production Ready Implementation"""

import json
import time
import uuid
from datetime import datetime
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

from utils.config import Config
from utils.data_models import RAGResponse, QueryType
from utils.evaluator import Evaluator
from utils.audit_logger import AuditLogger
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.query_rewriter import QueryRewriter
from retrieval.generator import Generator
from reranking.reranker import Reranker
from reranking.dynamic_cutoff import DynamicCutoff
from reranking.mmr_diversifier import MMRDiversifier


class UnifiedRAGSystem:
    """
    Production-ready RAG system with all best practices:
    - Query rewriting with step-back prompting
    - Hybrid search (Dense + BM25)
    - Cohere reranking
    - Dynamic chunk selection
    - MMR diversification
    - Quality evaluation
    - Comprehensive audit logging
    """
    
    def __init__(self):
        """Initialize the unified RAG system"""
        print("Initializing RAG System...")
        
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        with open(Config.CHUNKS_JSON, 'r', encoding='utf-8') as f:
            self.chunks_data = json.load(f)
        
        chroma_client = chromadb.PersistentClient(path=Config.CHROMA_PATH)
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=Config.OPENAI_API_KEY,
            model_name="text-embedding-3-large"
        )
        self.chroma_collection = chroma_client.get_collection(
            name=Config.COLLECTION_NAME,
            embedding_function=openai_ef
        )
        
        self.query_rewriter = QueryRewriter(self.openai_client) if Config.ENABLE_QUERY_REWRITING else None
        self.hybrid_retriever = HybridRetriever(self.chroma_collection, self.chunks_data)
        self.reranker = Reranker(api_key=Config.COHERE_API_KEY)
        self.generator = Generator(self.openai_client)
        self.evaluator = Evaluator(self.openai_client) if Config.ENABLE_EVALUATION else None
        self.audit_logger = AuditLogger() if Config.ENABLE_AUDIT else None
        
        print("RAG System initialized successfully")
        print(f"   - Query Rewriting: {'Enabled' if Config.ENABLE_QUERY_REWRITING else 'Disabled'}")
        print(f"   - Cohere Reranking: {'Enabled' if Config.COHERE_API_KEY else 'Disabled'}")
        print(f"   - MMR Diversification: {'Enabled' if Config.ENABLE_MMR else 'Disabled'}")
        print(f"   - Evaluation: {'Enabled' if Config.ENABLE_EVALUATION else 'Disabled'}")
        print(f"   - Audit Logging: {'Enabled' if Config.ENABLE_AUDIT else 'Disabled'}")
    
    def query(self, user_query: str, verbose: bool = True) -> RAGResponse:
        """
        Execute complete RAG pipeline
        
        Args:
            user_query: User's question
            verbose: Print progress information
            
        Returns:
            RAGResponse with answer and metadata
        """
        start_time = time.time()
        session_id = str(uuid.uuid4())
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"Unified RAG Query")
            print(f"{'='*80}")
            print(f"Query: {user_query}")
        
        analysis = self.query_rewriter.analyze_query(user_query) if self.query_rewriter else {
            "type": QueryType.FACTUAL,
            "expected_chunks": Config.FACTUAL_DEFAULT,
            "needs_rewriting": False
        }
        
        if verbose:
            print(f"\nAnalysis: {analysis['type'].value if isinstance(analysis['type'], QueryType) else analysis['type']}")
        
        retrieval_query = user_query
        query_rewritten = False
        
        if self.query_rewriter and Config.ENABLE_QUERY_REWRITING:
            rewrite_result = self.query_rewriter.rewrite(user_query, analysis)
            
            if rewrite_result["status"] == "rejected":
                return RAGResponse(
                    query=user_query,
                    answer=f"I cannot answer this query. {rewrite_result['reason']}\n\nSuggestion: {rewrite_result['suggestion']}",
                    query_type="rejected",
                    num_chunks_used=0,
                    chunks=[],
                    cutoff_reason="rejected",
                    latency_ms=(time.time() - start_time) * 1000,
                    session_id=session_id,
                    timestamp=datetime.now().isoformat()
                )
            
            if rewrite_result["use_stepback"]:
                retrieval_query = rewrite_result["stepback_query"]
                query_rewritten = True
                if verbose:
                    print(f"Rewritten: {retrieval_query}")
        
        candidates = self.hybrid_retriever.retrieve(retrieval_query, top_k=Config.INITIAL_CANDIDATES)
        if verbose:
            print(f"Retrieved: {len(candidates)} candidates")
        
        reranked = self.reranker.rerank(retrieval_query, candidates, top_k=Config.RERANK_TOP_K)
        if verbose:
            print(f"Reranked: Top {len(reranked)} (scores: {[f'{r.score:.3f}' for r in reranked[:5]]})")
        
        if Config.ENABLE_MMR and len(reranked) > 10:
            reranked = MMRDiversifier.diversify(reranked, k=min(20, len(reranked)))
            if verbose:
                print(f"MMR: Diversified to {len(reranked)} chunks")
        
        final_chunks, cutoff_reason = DynamicCutoff.determine_cutoff(
            reranked,
            analysis["expected_chunks"]
        )
        if verbose:
            print(f"Cutoff: {len(final_chunks)} chunks ({cutoff_reason})")
        
        context = self.generator.build_context(final_chunks)
        answer = self.generator.generate_answer(user_query, context)
        
        faithfulness_score = None
        if self.evaluator and Config.ENABLE_EVALUATION:
            faithfulness_score = self.evaluator.evaluate_faithfulness(answer, context)
            if verbose:
                print(f"Faithfulness: {faithfulness_score:.3f}")
        
        latency_ms = (time.time() - start_time) * 1000
        
        if self.audit_logger and Config.ENABLE_AUDIT:
            self.audit_logger.log({
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id,
                "query": user_query,
                "query_hash": self.audit_logger.hash_text(user_query),
                "query_rewritten": query_rewritten,
                "retrieval_query": retrieval_query,
                "query_type": analysis["type"].value if isinstance(analysis["type"], QueryType) else str(analysis["type"]),
                "num_chunks_used": len(final_chunks),
                "cutoff_reason": cutoff_reason,
                "faithfulness_score": faithfulness_score,
                "latency_ms": latency_ms,
                "answer_hash": self.audit_logger.hash_text(answer)
            })
        
        return RAGResponse(
            query=user_query,
            answer=answer,
            query_type=analysis["type"].value if isinstance(analysis['type'], QueryType) else str(analysis['type']),
            num_chunks_used=len(final_chunks),
            chunks=[{
                "id": c.chunk_id,
                "content": c.content,  # Added content field
                "score": c.score,
                "page": c.page,
                "rank": c.rank
            } for c in final_chunks],
            cutoff_reason=cutoff_reason,
            latency_ms=latency_ms,
            query_rewritten=query_rewritten,
            retrieval_query=retrieval_query,
            faithfulness_score=faithfulness_score,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )


def main():
    """Main function for testing"""
    print("=" * 80)
    print("Unified RAG System - Production Ready")
    print("=" * 80)
    
    rag = UnifiedRAGSystem()
    
    test_queries = [
        "What is the torque specification for the front shock absorber?",
        "Summarize all suspension inspection procedures",
        "How to replace the front coil spring?"
    ]
    
    print("\n" + "=" * 80)
    print("Running Test Queries")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print("=" * 80)
        
        result = rag.query(query, verbose=True)
        
        print(f"\nAnswer:")
        print(result.answer)
        
        print(f"\nMetadata:")
        print(f"   Query Type: {result.query_type}")
        print(f"   Chunks Used: {result.num_chunks_used}")
        print(f"   Cutoff Reason: {result.cutoff_reason}")
        print(f"   Latency: {result.latency_ms:.0f}ms")
        if result.faithfulness_score:
            print(f"   Faithfulness: {result.faithfulness_score:.3f}")
        print(f"   Source Pages: {[c['page'] for c in result.chunks]}")
    
    print("\n" + "=" * 80)
    print("Interactive Mode (type 'exit' to quit)")
    print("=" * 80)
    
    while True:
        user_input = input("\nYour question: ").strip()
        if user_input.lower() in ['exit', 'quit', 'q']:
            break
        
        if not user_input:
            continue
        
        result = rag.query(user_input, verbose=True)
        print(f"\nAnswer:\n{result.answer}")


if __name__ == "__main__":
    main()
