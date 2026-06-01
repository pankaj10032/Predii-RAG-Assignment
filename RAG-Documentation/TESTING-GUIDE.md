# Comprehensive Testing Guide

This guide explains how to run comprehensive tests on the RAG system using the 40-query test suite covering all 5 query types.

## 📋 Test Suite Overview

The comprehensive test suite includes **40 carefully crafted queries** across **5 query types**:

### Query Categories

| Category | Count | Keywords | Example |
|----------|-------|----------|---------|
| **📋 SUMMARY** | 5 | summarize, overview, list all | "Summarize all torque specifications for engine components" |
| **🔧 PROCEDURAL** | 10 | how to, steps, procedure | "How to replace the brake pads on this vehicle?" |
| **⚖️ COMPARISON** | 5 | compare, vs, difference | "Compare torque specs for cylinder head vs exhaust manifold bolts" |
| **⏳ TEMPORAL** | 5 | when, time, before, after | "When should the engine oil be changed?" |
| **❓ FACTUAL** | 15 | what is, specification | "What is the torque specification for cylinder head bolts?" |

## 🚀 Quick Start

### Method 1: Simple Test Runner (Recommended)

```bash
# Run the simple test runner
python run_comprehensive_test.py
```

**Or on Windows:**
```cmd
run_test.bat
```

### Method 2: Advanced Pipeline

```bash
# Using the advanced pipeline
python advanced-rag_pipeline.py --batch tests.txt --output comprehensive_results.json
```

### Method 3: Direct Comprehensive Test

```bash
# Run the full comprehensive test suite
python comprehensive_test.py
```

## 📊 Test Output

### Console Output
The test provides real-time progress and summary:

```
🧪 Running Comprehensive Test Suite
================================================================================
Total Queries: 40
Categories: 5

[ 1/40] Processing: Summarize all torque specifications for the engine...
   ✅ 2.34s | 8 chunks | summary | 0.923

[40/40] Processing: What is the recommended engine oil viscosity...
   ✅ 1.12s | 3 chunks | factual | 0.956

🎯 Test Completed Successfully!
================================================================================
Total Duration: 89.45s
Average Query Time: 2.24s
Queries per Second: 0.45
```

### JSON Output
Detailed results saved to timestamped JSON file:

```json
{
  "test_metadata": {
    "timestamp": "2026-06-01T17:30:00",
    "total_queries": 40,
    "categories": ["SUMMARY", "PROCEDURAL", "COMPARISON", "TEMPORAL", "FACTUAL"],
    "test_duration_seconds": 89.45,
    "system_config": {
      "query_rewriting_enabled": true,
      "cohere_reranking_enabled": true,
      "mmr_diversification_enabled": true
    }
  },
  "query_results": [
    {
      "query_id": 1,
      "query": "Summarize all torque specifications for the engine components.",
      "expected_category": "SUMMARY",
      "actual_query_type": "summary",
      "answer": "Based on the service manual...",
      "num_chunks_used": 8,
      "latency_ms": 2340,
      "faithfulness_score": 0.923,
      "category_match": true
    }
  ],
  "category_analysis": {
    "SUMMARY": {
      "total_queries": 5,
      "avg_latency_ms": 2156,
      "avg_chunks_used": 7.2,
      "avg_faithfulness": 0.891,
      "category_match_rate": 0.8
    }
  },
  "performance_metrics": {
    "latency": {
      "min_ms": 890,
      "max_ms": 3450,
      "avg_ms": 1876,
      "median_ms": 1650
    },
    "chunks": {
      "avg_chunks": 4.2,
      "total_chunks_retrieved": 168
    },
    "faithfulness": {
      "avg_score": 0.912
    }
  }
}
```

## 📈 Understanding Results

### Key Metrics

1. **Category Accuracy**: How well the system classifies query types
2. **Faithfulness Score**: Quality of answers (0.0-1.0)
3. **Latency**: Response time per query
4. **Chunk Usage**: Number of document chunks used
5. **Rewrite Rate**: Percentage of queries that were rewritten

### Performance Benchmarks

| Metric | Good | Excellent |
|--------|------|-----------|
| **Faithfulness** | > 0.80 | > 0.90 |
| **Category Accuracy** | > 70% | > 85% |
| **Avg Latency** | < 3000ms | < 2000ms |
| **Success Rate** | > 90% | > 95% |

## 🔧 Test Configuration

### Environment Setup

Ensure your `.env` file contains:
```
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
```

### System Requirements

- Python 3.8+
- All dependencies installed (`pip install -r requirements.txt`)
- ChromaDB populated with document chunks
- Sufficient API credits for 40 queries

## 📝 Test Files

### Core Files

1. **`tests.txt`** - 40 test queries (one per line)
2. **`comprehensive_test.py`** - Full test suite with analytics
3. **`run_comprehensive_test.py`** - Simple test runner
4. **`run_test.bat`** - Windows batch file

### Generated Files

- **`test_results_YYYYMMDD_HHMMSS.json`** - Timestamped results
- **`comprehensive_test_results_YYYYMMDD_HHMMSS.json`** - Detailed analytics

## 🎯 Test Scenarios

### Scenario 1: System Validation
**Purpose**: Verify system works correctly across all query types
```bash
python run_comprehensive_test.py
```

### Scenario 2: Performance Benchmarking
**Purpose**: Measure system performance and identify bottlenecks
```bash
python comprehensive_test.py
```

### Scenario 3: Configuration Testing
**Purpose**: Test different system configurations
```bash
# Modify config in utils/config.py, then run:
python comprehensive_test.py
```

### Scenario 4: Regression Testing
**Purpose**: Ensure changes don't break existing functionality
```bash
# Run before and after changes, compare results
python comprehensive_test.py
```

## 🔍 Analyzing Results

### Category Analysis

Check if the system correctly identifies query types:

```python
# From JSON results
category_analysis = results["category_analysis"]
for category, stats in category_analysis.items():
    print(f"{category}: {stats['category_match_rate']:.1%} accuracy")
```

### Performance Analysis

Identify performance patterns:

```python
# Analyze latency by category
for category, stats in category_analysis.items():
    print(f"{category}: {stats['avg_latency_ms']:.0f}ms avg latency")
```

### Quality Analysis

Assess answer quality:

```python
# Check faithfulness scores
performance = results["performance_metrics"]
print(f"Average faithfulness: {performance['faithfulness']['avg_score']:.3f}")
```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd RAG-Assignment
   python comprehensive_test.py
   ```

2. **API Key Issues**
   ```bash
   # Check .env file
   cat .env
   ```

3. **Missing Chunks**
   ```bash
   # Reprocess documents
   python -m preprocessing.embeddings
   ```

4. **Memory Issues**
   ```bash
   # Run with smaller batches
   python advanced-rag_pipeline.py --batch tests.txt --quiet
   ```

### Performance Issues

- **Slow queries**: Check API rate limits
- **High latency**: Consider reducing `INITIAL_CANDIDATES`
- **Low accuracy**: Verify document preprocessing

## 📊 Custom Testing

### Creating Custom Test Sets

1. **Create query file**:
   ```bash
   echo "Your custom query 1" > custom_tests.txt
   echo "Your custom query 2" >> custom_tests.txt
   ```

2. **Run custom tests**:
   ```bash
   python advanced-rag_pipeline.py --batch custom_tests.txt --output custom_results.json
   ```

### Modifying Test Categories

Edit `comprehensive_test.py` to add new categories:

```python
self.query_categories["NEW_CATEGORY"] = {
    "queries": list(range(41, 46)),  # Queries 41-45
    "keywords": ["custom", "keywords"],
    "expected_type": "new_category"
}
```

## 🎯 Best Practices

1. **Regular Testing**: Run comprehensive tests after any system changes
2. **Baseline Comparison**: Keep baseline results for comparison
3. **Category Coverage**: Ensure all query types are tested
4. **Performance Monitoring**: Track latency and accuracy trends
5. **Result Analysis**: Review failed queries to improve system

---

**Created**: June 1, 2026  
**For**: Ford F-150 Service Manual RAG System  
**Location**: `RAG-Assignment/RAG-Documentation/`