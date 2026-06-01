#!/usr/bin/env python3
"""
Comprehensive Test Suite for RAG System
Tests all 40 queries across 5 query types and saves detailed results
"""

import json
import time
import os
from datetime import datetime
from typing import List, Dict, Any
from unified_rag_system import UnifiedRAGSystem
from utils.data_models import QueryType


class ComprehensiveTestSuite:
    """
    Comprehensive test suite for RAG system with detailed analysis
    """
    
    def __init__(self):
        """Initialize the test suite"""
        print("🚀 Initializing Comprehensive Test Suite...")
        self.rag_system = UnifiedRAGSystem()
        
        # Query type mappings for analysis
        self.query_categories = {
            "SUMMARY": {
                "queries": list(range(1, 6)),  # Queries 1-5
                "keywords": ["summarize", "overview", "list all", "complete"],
                "expected_type": "summary"
            },
            "PROCEDURAL": {
                "queries": list(range(6, 16)),  # Queries 6-15
                "keywords": ["how to", "steps", "procedure", "install", "remove", "replace"],
                "expected_type": "procedural"
            },
            "COMPARISON": {
                "queries": list(range(16, 21)),  # Queries 16-20
                "keywords": ["compare", "vs", "versus", "difference", "between"],
                "expected_type": "comparison"
            },
            "TEMPORAL": {
                "queries": list(range(21, 26)),  # Queries 21-25
                "keywords": ["when", "date", "time", "year", "before", "after"],
                "expected_type": "temporal"
            },
            "FACTUAL": {
                "queries": list(range(26, 41)),  # Queries 26-40
                "keywords": ["what is", "specification", "rating", "capacity"],
                "expected_type": "factual"
            }
        }
        
        print("✅ Test suite initialized successfully!")
    
    def load_test_queries(self, filename: str = "tests.txt") -> List[str]:
        """Load test queries from file"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Test file '{filename}' not found")
        
        with open(filename, 'r', encoding='utf-8') as f:
            queries = [line.strip() for line in f if line.strip()]
        
        print(f"📋 Loaded {len(queries)} test queries from {filename}")
        return queries
    
    def run_comprehensive_test(self, queries: List[str]) -> Dict[str, Any]:
        """
        Run comprehensive test on all queries
        
        Args:
            queries: List of test queries
            
        Returns:
            Comprehensive test results
        """
        print(f"\n{'='*80}")
        print(f"🧪 Running Comprehensive Test Suite")
        print(f"{'='*80}")
        print(f"Total Queries: {len(queries)}")
        print(f"Categories: {len(self.query_categories)}")
        
        start_time = time.time()
        results = {
            "test_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_queries": len(queries),
                "categories": list(self.query_categories.keys()),
                "test_duration_seconds": 0,
                "system_config": self._get_system_config()
            },
            "query_results": [],
            "category_analysis": {},
            "performance_metrics": {},
            "summary_statistics": {}
        }
        
        # Process each query
        for i, query in enumerate(queries, 1):
            print(f"\n[{i:2d}/{len(queries)}] Processing: {query[:60]}...")
            
            query_start = time.time()
            rag_result = self.rag_system.query(query, verbose=False)
            query_duration = time.time() - query_start
            
            # Determine expected category
            expected_category = self._determine_query_category(i)
            
            # Create detailed result
            query_result = {
                "query_id": i,
                "query": query,
                "expected_category": expected_category,
                "actual_query_type": rag_result.query_type,
                "answer": rag_result.answer,
                "num_chunks_used": rag_result.num_chunks_used,
                "cutoff_reason": rag_result.cutoff_reason,
                "latency_ms": rag_result.latency_ms,
                "query_duration_seconds": query_duration,
                "query_rewritten": rag_result.query_rewritten,
                "retrieval_query": rag_result.retrieval_query,
                "faithfulness_score": rag_result.faithfulness_score,
                "source_pages": sorted(set(c['page'] for c in rag_result.chunks)),
                "chunk_details": rag_result.chunks,
                "session_id": rag_result.session_id,
                "timestamp": rag_result.timestamp,
                "category_match": expected_category.lower() == rag_result.query_type.lower()
            }
            
            results["query_results"].append(query_result)
            
            # Progress indicator
            print(f"   ✅ {query_duration:.2f}s | {rag_result.num_chunks_used} chunks | {rag_result.query_type} | {rag_result.faithfulness_score:.3f if rag_result.faithfulness_score else 'N/A'}")
        
        # Calculate comprehensive analytics
        total_duration = time.time() - start_time
        results["test_metadata"]["test_duration_seconds"] = total_duration
        
        results["category_analysis"] = self._analyze_by_category(results["query_results"])
        results["performance_metrics"] = self._calculate_performance_metrics(results["query_results"])
        results["summary_statistics"] = self._calculate_summary_statistics(results["query_results"])
        
        print(f"\n{'='*80}")
        print(f"🎯 Test Completed Successfully!")
        print(f"{'='*80}")
        print(f"Total Duration: {total_duration:.2f}s")
        print(f"Average Query Time: {total_duration/len(queries):.2f}s")
        print(f"Queries per Second: {len(queries)/total_duration:.2f}")
        
        return results
    
    def _determine_query_category(self, query_id: int) -> str:
        """Determine expected category for a query based on its ID"""
        for category, info in self.query_categories.items():
            if query_id in info["queries"]:
                return category
        return "UNKNOWN"
    
    def _analyze_by_category(self, query_results: List[Dict]) -> Dict[str, Any]:
        """Analyze results by query category"""
        category_stats = {}
        
        for category, info in self.query_categories.items():
            category_results = [r for r in query_results if r["expected_category"] == category]
            
            if category_results:
                category_stats[category] = {
                    "total_queries": len(category_results),
                    "avg_latency_ms": sum(r["latency_ms"] for r in category_results) / len(category_results),
                    "avg_chunks_used": sum(r["num_chunks_used"] for r in category_results) / len(category_results),
                    "avg_faithfulness": sum(r["faithfulness_score"] for r in category_results if r["faithfulness_score"]) / len([r for r in category_results if r["faithfulness_score"]]),
                    "category_match_rate": sum(1 for r in category_results if r["category_match"]) / len(category_results),
                    "query_rewrite_rate": sum(1 for r in category_results if r["query_rewritten"]) / len(category_results),
                    "cutoff_reasons": self._count_cutoff_reasons(category_results),
                    "query_types_detected": self._count_query_types(category_results)
                }
        
        return category_stats
    
    def _calculate_performance_metrics(self, query_results: List[Dict]) -> Dict[str, Any]:
        """Calculate overall performance metrics"""
        latencies = [r["latency_ms"] for r in query_results]
        chunks_used = [r["num_chunks_used"] for r in query_results]
        faithfulness_scores = [r["faithfulness_score"] for r in query_results if r["faithfulness_score"]]
        
        return {
            "latency": {
                "min_ms": min(latencies),
                "max_ms": max(latencies),
                "avg_ms": sum(latencies) / len(latencies),
                "median_ms": sorted(latencies)[len(latencies)//2]
            },
            "chunks": {
                "min_chunks": min(chunks_used),
                "max_chunks": max(chunks_used),
                "avg_chunks": sum(chunks_used) / len(chunks_used),
                "total_chunks_retrieved": sum(chunks_used)
            },
            "faithfulness": {
                "min_score": min(faithfulness_scores) if faithfulness_scores else None,
                "max_score": max(faithfulness_scores) if faithfulness_scores else None,
                "avg_score": sum(faithfulness_scores) / len(faithfulness_scores) if faithfulness_scores else None,
                "scores_available": len(faithfulness_scores)
            },
            "query_rewriting": {
                "total_rewrites": sum(1 for r in query_results if r["query_rewritten"]),
                "rewrite_rate": sum(1 for r in query_results if r["query_rewritten"]) / len(query_results)
            }
        }
    
    def _calculate_summary_statistics(self, query_results: List[Dict]) -> Dict[str, Any]:
        """Calculate summary statistics"""
        return {
            "total_queries_processed": len(query_results),
            "successful_queries": len([r for r in query_results if r["answer"] and "cannot answer" not in r["answer"].lower()]),
            "category_accuracy": sum(1 for r in query_results if r["category_match"]) / len(query_results),
            "avg_answer_length": sum(len(r["answer"]) for r in query_results) / len(query_results),
            "unique_source_pages": len(set().union(*[r["source_pages"] for r in query_results])),
            "cutoff_reason_distribution": self._count_cutoff_reasons(query_results),
            "query_type_distribution": self._count_query_types(query_results)
        }
    
    def _count_cutoff_reasons(self, results: List[Dict]) -> Dict[str, int]:
        """Count cutoff reasons"""
        reasons = {}
        for result in results:
            reason = result["cutoff_reason"]
            reasons[reason] = reasons.get(reason, 0) + 1
        return reasons
    
    def _count_query_types(self, results: List[Dict]) -> Dict[str, int]:
        """Count detected query types"""
        types = {}
        for result in results:
            query_type = result["actual_query_type"]
            types[query_type] = types.get(query_type, 0) + 1
        return types
    
    def _get_system_config(self) -> Dict[str, Any]:
        """Get current system configuration"""
        from utils.config import Config
        return {
            "query_rewriting_enabled": Config.ENABLE_QUERY_REWRITING,
            "cohere_reranking_enabled": bool(Config.COHERE_API_KEY),
            "mmr_diversification_enabled": Config.ENABLE_MMR,
            "evaluation_enabled": Config.ENABLE_EVALUATION,
            "audit_logging_enabled": Config.ENABLE_AUDIT,
            "initial_candidates": Config.INITIAL_CANDIDATES,
            "rerank_top_k": Config.RERANK_TOP_K
        }
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """Save test results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comprehensive_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {filename}")
        return filename
    
    def print_summary_report(self, results: Dict[str, Any]):
        """Print a comprehensive summary report"""
        print(f"\n{'='*80}")
        print(f"📊 COMPREHENSIVE TEST SUMMARY REPORT")
        print(f"{'='*80}")
        
        metadata = results["test_metadata"]
        performance = results["performance_metrics"]
        summary = results["summary_statistics"]
        
        print(f"\n🔧 Test Configuration:")
        print(f"   Total Queries: {metadata['total_queries']}")
        print(f"   Test Duration: {metadata['test_duration_seconds']:.2f}s")
        print(f"   Categories Tested: {', '.join(metadata['categories'])}")
        
        print(f"\n⚡ Performance Metrics:")
        print(f"   Avg Latency: {performance['latency']['avg_ms']:.0f}ms")
        print(f"   Latency Range: {performance['latency']['min_ms']:.0f}ms - {performance['latency']['max_ms']:.0f}ms")
        print(f"   Avg Chunks Used: {performance['chunks']['avg_chunks']:.1f}")
        print(f"   Chunks Range: {performance['chunks']['min_chunks']} - {performance['chunks']['max_chunks']}")
        if performance['faithfulness']['avg_score']:
            print(f"   Avg Faithfulness: {performance['faithfulness']['avg_score']:.3f}")
        
        print(f"\n🎯 Accuracy Metrics:")
        print(f"   Successful Queries: {summary['successful_queries']}/{summary['total_queries_processed']}")
        print(f"   Category Accuracy: {summary['category_accuracy']:.1%}")
        print(f"   Query Rewrite Rate: {performance['query_rewriting']['rewrite_rate']:.1%}")
        
        print(f"\n📋 Query Type Distribution:")
        for query_type, count in summary['query_type_distribution'].items():
            print(f"   {query_type}: {count} queries")
        
        print(f"\n📊 Category Analysis:")
        for category, stats in results["category_analysis"].items():
            print(f"   {category}:")
            print(f"      Queries: {stats['total_queries']}")
            print(f"      Avg Latency: {stats['avg_latency_ms']:.0f}ms")
            print(f"      Avg Chunks: {stats['avg_chunks_used']:.1f}")
            print(f"      Category Match: {stats['category_match_rate']:.1%}")
            print(f"      Faithfulness: {stats['avg_faithfulness']:.3f}")


def main():
    """Main function to run comprehensive tests"""
    print("🧪 Starting Comprehensive RAG System Test Suite")
    print("=" * 80)
    
    try:
        # Initialize test suite
        test_suite = ComprehensiveTestSuite()
        
        # Load test queries
        queries = test_suite.load_test_queries("tests.txt")
        
        # Run comprehensive test
        results = test_suite.run_comprehensive_test(queries)
        
        # Save results
        output_file = test_suite.save_results(results)
        
        # Print summary report
        test_suite.print_summary_report(results)
        
        print(f"\n{'='*80}")
        print(f"✅ Comprehensive test completed successfully!")
        print(f"📁 Results saved to: {output_file}")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        raise


if __name__ == "__main__":
    main()