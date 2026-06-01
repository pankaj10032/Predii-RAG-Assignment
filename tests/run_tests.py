"""
Test Runner for RAG System
Runs all tests and generates a comprehensive report
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from datetime import datetime


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def run_benchmark():
    """Run benchmark tests"""
    print_header("BENCHMARK TESTS")
    
    try:
        from tests.benchmark_rag import main as benchmark_main
        print("\nRunning benchmarks...")
        benchmark_main()
        return True
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        return False


def run_comparison():
    """Run comparison tests"""
    print_header("COMPARISON TESTS")
    
    try:
        from tests.compare_approaches import main as compare_main
        print("\nRunning comparison...")
        compare_main()
        return True
    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        return False


def run_evaluation():
    """Run evaluation framework"""
    print_header("EVALUATION FRAMEWORK")
    
    try:
        from tests.evaluation_framework import main as eval_main
        print("\nRunning evaluation...")
        eval_main()
        return True
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        return False


def main():
    """Run all tests"""
    print("="*80)
    print("  RAG SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    start_time = time.time()
    results = {}
    
    # Run tests
    print("\n📋 Running test suite...")
    
    results['benchmark'] = run_benchmark()
    results['comparison'] = run_comparison()
    results['evaluation'] = run_evaluation()
    
    # Summary
    total_time = time.time() - start_time
    
    print_header("TEST SUMMARY")
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name.capitalize():20s}: {status}")
    
    passed_count = sum(1 for p in results.values() if p)
    total_count = len(results)
    
    print(f"\n  Total: {passed_count}/{total_count} tests passed")
    print(f"  Time: {total_time:.2f}s")
    
    if passed_count == total_count:
        print("\n  🎉 ALL TESTS PASSED!")
    else:
        print(f"\n  ⚠️  {total_count - passed_count} test(s) failed")
    
    print("\n" + "="*80)
    print(f"  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    return passed_count == total_count


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
