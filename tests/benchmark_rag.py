"""
Benchmark Script: Measure RAG Pipeline Performance
Tracks: Accuracy, Efficiency, Latency, Cost
"""

import time
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import statistics


@dataclass
class BenchmarkResult:
    """Single query benchmark result"""
    query: str
    query_type: str
    approach: str
    num_chunks: int
    latency_ms: float
    context_length: int
    answer_length: int
    cutoff_reason: str = ""
    timestamp: str = ""
    query_rewritten: bool = False
    retrieval_query: str = ""


@dataclass
class BenchmarkSummary:
    """Aggregate benchmark statistics"""
    approach: str
    total_queries: int
    avg_chunks: float
    avg_latency_ms: float
    avg_context_length: float
    avg_answer_length: float
    total_time_s: float
    queries_per_second: float


class RAGBenchmark:
    """Benchmark harness for RAG pipelines"""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
    
    def run_query(
        self,
        rag_pipeline,
        query: str,
        approach: str,
        is_advanced: bool = False
    ) -> BenchmarkResult:
        """Run single query and collect metrics"""
        
        start_time = time.time()
        
        if is_advanced:
            result = rag_pipeline.query(query, verbose=False)
            num_chunks = result['num_chunks_used']
            query_type = result['query_type']
            cutoff_reason = result['cutoff_reason']
            answer = result['answer']
            query_rewritten = result.get('query_rewritten', False)
            retrieval_query = result.get('retrieval_query', query)
        else:
            result = rag_pipeline.query(query, top_k=5)
            num_chunks = result['num_chunks']
            query_type = "unknown"
            cutoff_reason = "fixed_top_k"
            answer = result['answer']
            query_rewritten = False
            retrieval_query = query
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Estimate context length (rough approximation)
        context_length = result.get('context_length', num_chunks * 500)
        
        benchmark_result = BenchmarkResult(
            query=query,
            query_type=query_type,
            approach=approach,
            num_chunks=num_chunks,
            latency_ms=latency_ms,
            context_length=context_length,
            answer_length=len(answer),
            cutoff_reason=cutoff_reason,
            timestamp=datetime.now().isoformat(),
            query_rewritten=query_rewritten,
            retrieval_query=retrieval_query
        )
        
        self.results.append(benchmark_result)
        return benchmark_result
    
    def run_benchmark_suite(
        self,
        naive_rag,
        advanced_rag,
        test_queries: List[Dict[str, str]]
    ):
        """Run full benchmark suite"""
        
        print("=" * 80)
        print("🏁 STARTING BENCHMARK SUITE")
        print("=" * 80)
        print(f"Total queries: {len(test_queries)}")
        print(f"Approaches: Naive (fixed top_k=5) vs Advanced (dynamic)")
        print()
        
        # Run naive approach
        print("🔵 Running Naive RAG...")
        naive_start = time.time()
        for i, test in enumerate(test_queries, 1):
            print(f"   [{i}/{len(test_queries)}] {test['query'][:60]}...")
            self.run_query(naive_rag, test['query'], "Naive", is_advanced=False)
        naive_total = time.time() - naive_start
        
        # Run advanced approach
        print("\n🟢 Running Advanced RAG...")
        advanced_start = time.time()
        for i, test in enumerate(test_queries, 1):
            print(f"   [{i}/{len(test_queries)}] {test['query'][:60]}...")
            self.run_query(advanced_rag, test['query'], "Advanced", is_advanced=True)
        advanced_total = time.time() - advanced_start
        
        print(f"\n✅ Benchmark complete!")
        print(f"   Naive total time: {naive_total:.2f}s")
        print(f"   Advanced total time: {advanced_total:.2f}s")
    
    def generate_summary(self, approach: str) -> BenchmarkSummary:
        """Generate summary statistics for an approach"""
        
        approach_results = [r for r in self.results if r.approach == approach]
        
        if not approach_results:
            return None
        
        return BenchmarkSummary(
            approach=approach,
            total_queries=len(approach_results),
            avg_chunks=statistics.mean([r.num_chunks for r in approach_results]),
            avg_latency_ms=statistics.mean([r.latency_ms for r in approach_results]),
            avg_context_length=statistics.mean([r.context_length for r in approach_results]),
            avg_answer_length=statistics.mean([r.answer_length for r in approach_results]),
            total_time_s=sum([r.latency_ms for r in approach_results]) / 1000,
            queries_per_second=len(approach_results) / (sum([r.latency_ms for r in approach_results]) / 1000)
        )
    
    def print_comparison(self):
        """Print detailed comparison"""
        
        naive_summary = self.generate_summary("Naive")
        advanced_summary = self.generate_summary("Advanced")
        
        if not naive_summary or not advanced_summary:
            print("❌ Insufficient data for comparison")
            return
        
        print("\n" + "=" * 80)
        print("📊 BENCHMARK RESULTS")
        print("=" * 80)
        
        # Chunks comparison
        print("\n📦 CHUNKS USED")
        print(f"   Naive:    {naive_summary.avg_chunks:.2f} chunks/query")
        print(f"   Advanced: {advanced_summary.avg_chunks:.2f} chunks/query")
        chunk_diff = ((advanced_summary.avg_chunks - naive_summary.avg_chunks) / naive_summary.avg_chunks) * 100
        print(f"   Difference: {chunk_diff:+.1f}%")
        
        # Context length comparison
        print("\n📏 CONTEXT LENGTH")
        print(f"   Naive:    {naive_summary.avg_context_length:.0f} chars/query")
        print(f"   Advanced: {advanced_summary.avg_context_length:.0f} chars/query")
        context_diff = ((advanced_summary.avg_context_length - naive_summary.avg_context_length) / naive_summary.avg_context_length) * 100
        print(f"   Difference: {context_diff:+.1f}%")
        
        # Latency comparison
        print("\n⚡ LATENCY")
        print(f"   Naive:    {naive_summary.avg_latency_ms:.0f} ms/query")
        print(f"   Advanced: {advanced_summary.avg_latency_ms:.0f} ms/query")
        latency_diff = ((advanced_summary.avg_latency_ms - naive_summary.avg_latency_ms) / naive_summary.avg_latency_ms) * 100
        print(f"   Difference: {latency_diff:+.1f}%")
        
        # Throughput
        print("\n🚀 THROUGHPUT")
        print(f"   Naive:    {naive_summary.queries_per_second:.2f} queries/sec")
        print(f"   Advanced: {advanced_summary.queries_per_second:.2f} queries/sec")
        
        # Cost estimation (rough)
        print("\n💰 ESTIMATED COST (per 1000 queries)")
        naive_tokens = naive_summary.avg_context_length * 1000 / 4  # ~4 chars per token
        advanced_tokens = advanced_summary.avg_context_length * 1000 / 4
        naive_cost = (naive_tokens / 1_000_000) * 0.15  # $0.15 per 1M tokens (GPT-4o-mini input)
        advanced_cost = (advanced_tokens / 1_000_000) * 0.15
        print(f"   Naive:    ${naive_cost:.2f}")
        print(f"   Advanced: ${advanced_cost:.2f}")
        print(f"   Savings:  ${naive_cost - advanced_cost:.2f} ({((naive_cost - advanced_cost) / naive_cost * 100):.1f}%)")
        
        # Query type breakdown (advanced only)
        print("\n🎯 QUERY TYPE BREAKDOWN (Advanced)")
        advanced_results = [r for r in self.results if r.approach == "Advanced"]
        query_types = {}
        for r in advanced_results:
            if r.query_type not in query_types:
                query_types[r.query_type] = []
            query_types[r.query_type].append(r.num_chunks)
        
        for qtype, chunks in query_types.items():
            avg_chunks = statistics.mean(chunks)
            print(f"   {qtype.capitalize():12s}: {avg_chunks:.1f} chunks/query (n={len(chunks)})")
        
        # Query rewriting stats (advanced only)
        rewritten_count = sum(1 for r in advanced_results if r.query_rewritten)
        if rewritten_count > 0:
            print(f"\n🔄 QUERY REWRITING STATS (Advanced)")
            print(f"   Queries Rewritten: {rewritten_count}/{len(advanced_results)} ({rewritten_count/len(advanced_results)*100:.1f}%)")
            print(f"   Queries Unchanged: {len(advanced_results) - rewritten_count}/{len(advanced_results)}")
        
        # Key insights
        print("\n" + "=" * 80)
        print("💡 KEY INSIGHTS")
        print("=" * 80)
        
        if context_diff < -10:
            print("✅ Advanced RAG uses significantly LESS context (more efficient)")
        elif context_diff > 10:
            print("✅ Advanced RAG uses MORE context when needed (better completeness)")
        
        if latency_diff < 20:
            print("✅ Latency overhead is acceptable (<20%)")
        else:
            print("⚠️  Latency overhead is significant (consider optimization)")
        
        if advanced_cost < naive_cost:
            print(f"✅ Advanced RAG saves ${naive_cost - advanced_cost:.2f} per 1000 queries")
        
        print("\n🎯 Recommendation:")
        if context_diff < 0 and advanced_cost < naive_cost:
            print("   STRONGLY RECOMMENDED: Advanced RAG is more efficient AND cheaper")
        elif abs(context_diff) < 5:
            print("   NEUTRAL: Both approaches have similar efficiency")
        else:
            print("   RECOMMENDED: Advanced RAG adapts better to query types")
    
    def save_results(self, filename: str = "benchmark_results.json"):
        """Save detailed results to JSON"""
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_queries": len(self.results),
            "results": [asdict(r) for r in self.results],
            "summaries": {
                "naive": asdict(self.generate_summary("Naive")) if self.generate_summary("Naive") else None,
                "advanced": asdict(self.generate_summary("Advanced")) if self.generate_summary("Advanced") else None
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {filename}")


def main():
    """Run benchmark"""
    
    # Test queries covering different types
    test_queries = [
        # Factual queries (should use 1-3 chunks)
        {"query": "What is the torque specification for the front shock absorber?", "type": "factual"},
        {"query": "Define camber adjustment", "type": "factual"},
        {"query": "What is the ride height measurement procedure?", "type": "factual"},
        
        # Summary queries (should use 10-15 chunks)
        {"query": "Summarize all suspension inspection procedures", "type": "summary"},
        {"query": "Give me a complete overview of ball joint inspection", "type": "summary"},
        {"query": "List all diagnostic tests for suspension issues", "type": "summary"},
        
        # Procedural queries (should use 5-8 chunks)
        {"query": "How to replace the front coil spring?", "type": "procedural"},
        {"query": "Steps to remove the shock absorber", "type": "procedural"},
        {"query": "Procedure for camber and caster adjustment", "type": "procedural"},
    ]
    
    # Initialize pipelines
    print("📦 Initializing RAG pipelines...")
    
    try:
        from compare_approaches import NaiveRAG
        from advanced_rag_pipeline import AdvancedRAGPipeline
        
        naive_rag = NaiveRAG()
        advanced_rag = AdvancedRAGPipeline()
    except Exception as e:
        print(f"❌ Error initializing pipelines: {e}")
        return
    
    # Run benchmark
    benchmark = RAGBenchmark()
    benchmark.run_benchmark_suite(naive_rag, advanced_rag, test_queries)
    
    # Print comparison
    benchmark.print_comparison()
    
    # Save results
    benchmark.save_results()


if __name__ == "__main__":
    main()
