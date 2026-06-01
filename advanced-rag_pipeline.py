#!/usr/bin/env python3
"""
Advanced RAG Pipeline - Enhanced Terminal Interface
Production-ready RAG system with comprehensive CLI testing capabilities
"""

import argparse
import json
import sys
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

from unified_rag_system import UnifiedRAGSystem
from utils.config import Config
from utils.data_models import RAGResponse


class AdvancedRAGPipeline:
    """
    Enhanced RAG Pipeline with advanced terminal interface capabilities
    """
    
    def __init__(self, verbose: bool = True):
        """Initialize the advanced RAG pipeline"""
        self.verbose = verbose
        self.rag_system = UnifiedRAGSystem()
        self.query_history = []
        
        if self.verbose:
            print("🚀 Advanced RAG Pipeline initialized successfully!")
    
    def single_query(self, query: str, show_chunks: bool = False, show_metadata: bool = True) -> RAGResponse:
        """
        Execute a single query with detailed output
        
        Args:
            query: User question
            show_chunks: Whether to display retrieved chunks
            show_metadata: Whether to display metadata
            
        Returns:
            RAGResponse object
        """
        if self.verbose:
            print(f"\n{'='*80}")
            print(f"🔍 Processing Query")
            print(f"{'='*80}")
            print(f"Query: {query}")
        
        start_time = time.time()
        result = self.rag_system.query(query, verbose=self.verbose)
        
        # Store in history
        self.query_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'result': result
        })
        
        # Display results
        print(f"\n📝 Answer:")
        print("-" * 40)
        print(result.answer)
        
        if show_metadata:
            self._display_metadata(result)
        
        if show_chunks:
            self._display_chunks(result)
        
        return result
    
    def batch_query(self, queries: List[str], output_file: Optional[str] = None) -> List[RAGResponse]:
        """
        Execute multiple queries in batch mode
        
        Args:
            queries: List of queries to process
            output_file: Optional file to save results
            
        Returns:
            List of RAGResponse objects
        """
        results = []
        
        print(f"\n🔄 Batch Processing {len(queries)} queries...")
        print("=" * 80)
        
        for i, query in enumerate(queries, 1):
            print(f"\n[{i}/{len(queries)}] Processing: {query[:60]}...")
            
            result = self.rag_system.query(query, verbose=False)
            results.append(result)
            
            # Brief summary
            print(f"   ✅ Answered ({result.num_chunks_used} chunks, {result.latency_ms:.0f}ms)")
            if result.faithfulness_score:
                print(f"   📊 Faithfulness: {result.faithfulness_score:.3f}")
        
        # Save results if requested
        if output_file:
            self._save_batch_results(results, output_file)
            print(f"\n💾 Results saved to: {output_file}")
        
        return results
    
    def interactive_mode(self):
        """
        Start interactive query mode
        """
        print(f"\n{'='*80}")
        print("🎯 Interactive RAG Mode")
        print("=" * 80)
        print("Commands:")
        print("  - Type your question to get an answer")
        print("  - 'history' - Show query history")
        print("  - 'stats' - Show session statistics")
        print("  - 'config' - Show current configuration")
        print("  - 'clear' - Clear history")
        print("  - 'help' - Show this help")
        print("  - 'exit' or 'quit' - Exit interactive mode")
        print("=" * 80)
        
        while True:
            try:
                user_input = input("\n🤖 RAG> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif user_input.lower() == 'history':
                    self._show_history()
                
                elif user_input.lower() == 'stats':
                    self._show_stats()
                
                elif user_input.lower() == 'config':
                    self._show_config()
                
                elif user_input.lower() == 'clear':
                    self.query_history.clear()
                    print("🗑️ History cleared!")
                
                elif user_input.lower() == 'help':
                    self._show_help()
                
                else:
                    # Process as query
                    self.single_query(user_input, show_chunks=True, show_metadata=True)
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def benchmark_mode(self, test_queries: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run benchmark tests on the RAG system
        
        Args:
            test_queries: Optional list of test queries
            
        Returns:
            Benchmark results dictionary
        """
        if test_queries is None:
            test_queries = [
                "What is the torque specification for the front shock absorber?",
                "How to replace the front coil spring?",
                "Summarize all suspension inspection procedures",
                "What are the safety precautions for suspension work?",
                "List all tools required for shock absorber replacement",
                "What is the procedure for wheel alignment after suspension repair?",
                "How to diagnose suspension noise issues?",
                "What are the common suspension problems in Ford F-150?"
            ]
        
        print(f"\n🏁 Benchmark Mode - Testing {len(test_queries)} queries")
        print("=" * 80)
        
        results = []
        total_time = 0
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n[{i}/{len(test_queries)}] {query}")
            
            start_time = time.time()
            result = self.rag_system.query(query, verbose=False)
            query_time = time.time() - start_time
            total_time += query_time
            
            results.append(result)
            
            print(f"   ⏱️  {query_time:.2f}s | 📊 {result.num_chunks_used} chunks | 🎯 {result.faithfulness_score:.3f if result.faithfulness_score else 'N/A'}")
        
        # Calculate statistics
        avg_latency = sum(r.latency_ms for r in results) / len(results)
        avg_chunks = sum(r.num_chunks_used for r in results) / len(results)
        avg_faithfulness = sum(r.faithfulness_score for r in results if r.faithfulness_score) / len([r for r in results if r.faithfulness_score])
        
        benchmark_results = {
            'total_queries': len(test_queries),
            'total_time': total_time,
            'avg_latency_ms': avg_latency,
            'avg_chunks_used': avg_chunks,
            'avg_faithfulness': avg_faithfulness,
            'queries_per_second': len(test_queries) / total_time,
            'results': results
        }
        
        # Display summary
        print(f"\n📈 Benchmark Results")
        print("=" * 40)
        print(f"Total Queries: {benchmark_results['total_queries']}")
        print(f"Total Time: {benchmark_results['total_time']:.2f}s")
        print(f"Avg Latency: {benchmark_results['avg_latency_ms']:.0f}ms")
        print(f"Avg Chunks: {benchmark_results['avg_chunks_used']:.1f}")
        print(f"Avg Faithfulness: {benchmark_results['avg_faithfulness']:.3f}")
        print(f"Queries/Second: {benchmark_results['queries_per_second']:.2f}")
        
        return benchmark_results
    
    def _display_metadata(self, result: RAGResponse):
        """Display query metadata"""
        print(f"\n📊 Metadata:")
        print("-" * 40)
        print(f"Query Type: {result.query_type}")
        print(f"Chunks Used: {result.num_chunks_used}")
        print(f"Cutoff Reason: {result.cutoff_reason}")
        print(f"Latency: {result.latency_ms:.0f}ms")
        if result.faithfulness_score:
            print(f"Faithfulness: {result.faithfulness_score:.3f}")
        if result.query_rewritten:
            print(f"Query Rewritten: Yes")
            print(f"Retrieval Query: {result.retrieval_query}")
        print(f"Source Pages: {sorted(set(c['page'] for c in result.chunks))}")
    
    def _display_chunks(self, result: RAGResponse):
        """Display retrieved chunks information"""
        print(f"\n📚 Retrieved Chunks ({len(result.chunks)}):")
        print("-" * 40)
        for i, chunk in enumerate(result.chunks[:5], 1):  # Show top 5
            print(f"{i}. ID: {chunk['id']} | Page: {chunk['page']} | Score: {chunk['score']:.3f}")
        if len(result.chunks) > 5:
            print(f"... and {len(result.chunks) - 5} more chunks")
    
    def _show_history(self):
        """Show query history"""
        if not self.query_history:
            print("📝 No queries in history")
            return
        
        print(f"\n📝 Query History ({len(self.query_history)} queries):")
        print("-" * 80)
        for i, entry in enumerate(self.query_history[-10:], 1):  # Show last 10
            result = entry['result']
            print(f"{i}. {entry['query'][:60]}...")
            print(f"   ⏱️ {result.latency_ms:.0f}ms | 📊 {result.num_chunks_used} chunks | 🎯 {result.faithfulness_score:.3f if result.faithfulness_score else 'N/A'}")
    
    def _show_stats(self):
        """Show session statistics"""
        if not self.query_history:
            print("📊 No statistics available")
            return
        
        results = [entry['result'] for entry in self.query_history]
        
        print(f"\n📊 Session Statistics:")
        print("-" * 40)
        print(f"Total Queries: {len(results)}")
        print(f"Avg Latency: {sum(r.latency_ms for r in results) / len(results):.0f}ms")
        print(f"Avg Chunks: {sum(r.num_chunks_used for r in results) / len(results):.1f}")
        
        if any(r.faithfulness_score for r in results):
            faithful_scores = [r.faithfulness_score for r in results if r.faithfulness_score]
            print(f"Avg Faithfulness: {sum(faithful_scores) / len(faithful_scores):.3f}")
        
        # Query type distribution
        query_types = {}
        for result in results:
            query_types[result.query_type] = query_types.get(result.query_type, 0) + 1
        
        print(f"Query Types: {dict(query_types)}")
    
    def _show_config(self):
        """Show current configuration"""
        print(f"\n⚙️ Current Configuration:")
        print("-" * 40)
        print(f"Query Rewriting: {'Enabled' if Config.ENABLE_QUERY_REWRITING else 'Disabled'}")
        print(f"Cohere Reranking: {'Enabled' if Config.COHERE_API_KEY else 'Disabled'}")
        print(f"MMR Diversification: {'Enabled' if Config.ENABLE_MMR else 'Disabled'}")
        print(f"Evaluation: {'Enabled' if Config.ENABLE_EVALUATION else 'Disabled'}")
        print(f"Audit Logging: {'Enabled' if Config.ENABLE_AUDIT else 'Disabled'}")
        print(f"Initial Candidates: {Config.INITIAL_CANDIDATES}")
        print(f"Rerank Top K: {Config.RERANK_TOP_K}")
    
    def _show_help(self):
        """Show help information"""
        print(f"\n❓ Help - Available Commands:")
        print("-" * 40)
        print("• Type any question to get an answer")
        print("• 'history' - Show recent queries")
        print("• 'stats' - Show session statistics")
        print("• 'config' - Show system configuration")
        print("• 'clear' - Clear query history")
        print("• 'exit' or 'quit' - Exit interactive mode")
    
    def _save_batch_results(self, results: List[RAGResponse], filename: str):
        """Save batch results to file"""
        output_data = []
        for result in results:
            output_data.append({
                'query': result.query,
                'answer': result.answer,
                'query_type': result.query_type,
                'num_chunks_used': result.num_chunks_used,
                'latency_ms': result.latency_ms,
                'faithfulness_score': result.faithfulness_score,
                'timestamp': result.timestamp
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Advanced RAG Pipeline - Enhanced Terminal Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python advanced-rag_pipeline.py --interactive
  python advanced-rag_pipeline.py --query "What is the torque specification?"
  python advanced-rag_pipeline.py --benchmark
  python advanced-rag_pipeline.py --batch queries.txt --output results.json
        """
    )
    
    parser.add_argument('--query', '-q', type=str, help='Single query to process')
    parser.add_argument('--interactive', '-i', action='store_true', help='Start interactive mode')
    parser.add_argument('--benchmark', '-b', action='store_true', help='Run benchmark tests')
    parser.add_argument('--batch', type=str, help='File containing queries (one per line)')
    parser.add_argument('--output', '-o', type=str, help='Output file for batch results')
    parser.add_argument('--chunks', '-c', action='store_true', help='Show retrieved chunks')
    parser.add_argument('--no-metadata', action='store_true', help='Hide metadata')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = AdvancedRAGPipeline(verbose=not args.quiet)
    
    try:
        if args.query:
            # Single query mode
            pipeline.single_query(
                args.query, 
                show_chunks=args.chunks, 
                show_metadata=not args.no_metadata
            )
        
        elif args.batch:
            # Batch mode
            if not os.path.exists(args.batch):
                print(f"❌ Error: File '{args.batch}' not found")
                sys.exit(1)
            
            with open(args.batch, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip()]
            
            pipeline.batch_query(queries, args.output)
        
        elif args.benchmark:
            # Benchmark mode
            pipeline.benchmark_mode()
        
        elif args.interactive:
            # Interactive mode
            pipeline.interactive_mode()
        
        else:
            # Default: show help and start interactive mode
            parser.print_help()
            print("\n🚀 Starting interactive mode...")
            pipeline.interactive_mode()
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()