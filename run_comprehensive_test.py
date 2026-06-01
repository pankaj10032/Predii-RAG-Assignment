#!/usr/bin/env python3
"""
Quick Test Runner for Comprehensive RAG System Testing
Simple wrapper to run all 40 test queries and save results
"""

import os
import sys
from datetime import datetime
from comprehensive_test import ComprehensiveTestSuite


def main():
    """Run comprehensive test with simple interface"""
    print("RAG System - Comprehensive Test Runner")
    print("=" * 60)
    print("This will run all 40 test queries across 5 categories:")
    print("  SUMMARY (5 queries)")
    print("  PROCEDURAL (10 queries)")
    print("  COMPARISON (5 queries)")
    print("  TEMPORAL (5 queries)")
    print("  FACTUAL (15 queries)")
    print("=" * 60)

    if not os.path.exists("tests.txt"):
        print("Error: tests.txt file not found!")
        print("Please ensure tests.txt is in the current directory.")
        sys.exit(1)

    try:
        print("\nInitializing test suite...")
        test_suite = ComprehensiveTestSuite()

        print("Loading test queries...")
        queries = test_suite.load_test_queries("tests.txt")

        print(f"Running {len(queries)} test queries...")
        print("This may take several minutes depending on your system...")

        results = test_suite.run_comprehensive_test(queries)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"test_results_{timestamp}.json"

        test_suite.save_results(results, output_file)
        test_suite.print_summary_report(results)

        print(f"\n{'='*60}")
        print("Test completed successfully!")
        print(f"Detailed results saved to: {output_file}")
        print("You can analyze the JSON file for detailed metrics")
        print("=" * 60)

        metadata = results["test_metadata"]
        performance = results["performance_metrics"]
        summary = results["summary_statistics"]

        print("\nQuick Summary:")
        print(f"   Total Time: {metadata['test_duration_seconds']:.1f}s")
        print(f"   Success Rate: {summary['successful_queries']}/{summary['total_queries_processed']}")
        print(f"   Avg Latency: {performance['latency']['avg_ms']:.0f}ms")
        print(f"   Avg Faithfulness: {performance['faithfulness']['avg_score']:.3f if performance['faithfulness']['avg_score'] else 'N/A'}")
        print(f"   Avg Chunks: {performance['chunks']['avg_chunks']:.1f}")

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during testing: {e}")
        print("Please check your system configuration and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
