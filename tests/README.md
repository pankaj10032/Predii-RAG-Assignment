# RAG System Tests

This folder contains all test, benchmark, and evaluation scripts for the RAG system.

## Test Files

### Benchmarks
- **`benchmark_rag.py`** - Performance benchmarking suite
  - Measures latency, accuracy, cost
  - Compares naive vs advanced approaches
  - Generates detailed reports

### Comparisons
- **`compare_approaches.py`** - Side-by-side comparison
  - Naive (fixed top_k=5) vs Advanced (dynamic)
  - Shows improvements in accuracy and cost
  - Demonstrates query-specific adaptations

### Evaluation
- **`evaluation_framework.py`** - Comprehensive evaluation
  - Golden dataset evaluation
  - LLM-as-judge metrics
  - Drift detection
  - Multi-dimensional quality assessment

## Running Tests

### Run All Tests
```bash
cd tests
python run_tests.py
```

### Run Individual Tests
```bash
# Benchmarks
python benchmark_rag.py

# Comparison
python compare_approaches.py

# Evaluation
python evaluation_framework.py
```

### From Parent Directory
```bash
python -m tests.run_tests
```

## Test Results

Tests generate the following outputs:
- `benchmark_results.json` - Detailed benchmark data
- Console output with formatted reports
- Performance metrics and comparisons

## Expected Results

### Benchmark Tests
- ✅ Latency measurements
- ✅ Accuracy comparisons
- ✅ Cost analysis
- ✅ Query type breakdown

### Comparison Tests
- ✅ Naive vs Advanced comparison
- ✅ Chunk usage analysis
- ✅ Cost savings calculation

### Evaluation Tests
- ✅ Faithfulness scoring
- ✅ Citation accuracy
- ✅ Retrieval quality metrics

## Troubleshooting

### Issue: Import errors
**Solution**: Run from parent directory or ensure parent is in PYTHONPATH

### Issue: Missing dependencies
**Solution**: `pip install -r ../requirements.txt`

### Issue: No results
**Solution**: Ensure ChromaDB is populated with chunks

---

**Location**: `RAG-Assignment/tests/`  
**Last Updated**: June 1, 2026
