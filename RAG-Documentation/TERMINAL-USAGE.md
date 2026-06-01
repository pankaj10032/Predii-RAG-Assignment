# Terminal Usage Guide

This guide explains how to use the `advanced-rag_pipeline.py` for comprehensive terminal-based testing of the RAG system.

## Overview

The `advanced-rag_pipeline.py` provides a powerful command-line interface with multiple modes:

- **Single Query Mode**: Execute individual queries with detailed output
- **Interactive Mode**: Real-time query interface with history and statistics
- **Batch Mode**: Process multiple queries from a file
- **Benchmark Mode**: Performance testing with predefined queries

## Installation & Setup

Ensure you have the RAG system properly set up:

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables in .env
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key

# Ensure chunks are processed (first time only)
python -m preprocessing.embeddings
```

## Usage Modes

### 1. Interactive Mode (Recommended)

Start an interactive session for real-time querying:

```bash
python advanced-rag_pipeline.py --interactive
```

**Interactive Commands:**
- Type any question to get an answer
- `history` - Show recent queries and results
- `stats` - Display session statistics
- `config` - Show current system configuration
- `clear` - Clear query history
- `help` - Show available commands
- `exit` or `quit` - Exit interactive mode

### 2. Single Query Mode

Execute a single query with detailed output:

```bash
# Basic query
python advanced-rag_pipeline.py --query "What is the torque specification for the front shock absorber?"

# Show retrieved chunks
python advanced-rag_pipeline.py --query "How to replace front coil spring?" --chunks

# Hide metadata for cleaner output
python advanced-rag_pipeline.py --query "Suspension inspection procedures" --no-metadata
```

### 3. Batch Processing Mode

Process multiple queries from a text file:

```bash
# Create a queries file (queries.txt)
echo "What is the torque specification for the front shock absorber?" > queries.txt
echo "How to replace the front coil spring?" >> queries.txt
echo "Summarize all suspension inspection procedures" >> queries.txt

# Process batch with output file
python advanced-rag_pipeline.py --batch queries.txt --output results.json

# Process batch without saving
python advanced-rag_pipeline.py --batch queries.txt
```

### 4. Benchmark Mode

Run performance benchmarks with predefined test queries:

```bash
python advanced-rag_pipeline.py --benchmark
```

This will test 8 predefined queries and provide:
- Average latency
- Average chunks used
- Average faithfulness score
- Queries per second
- Detailed per-query metrics

## Command Line Options

```bash
python advanced-rag_pipeline.py [OPTIONS]

Options:
  -q, --query TEXT        Single query to process
  -i, --interactive       Start interactive mode
  -b, --benchmark         Run benchmark tests
  --batch FILE           File containing queries (one per line)
  -o, --output FILE      Output file for batch results
  -c, --chunks           Show retrieved chunks
  --no-metadata          Hide metadata
  --quiet                Minimal output
  -h, --help             Show help message
```

## Example Usage Sessions

### Example 1: Quick Testing

```bash
# Test a single query with full details
python advanced-rag_pipeline.py -q "What tools are needed for shock replacement?" -c

# Output includes:
# - Answer
# - Metadata (query type, chunks used, latency, faithfulness)
# - Retrieved chunks (IDs, pages, scores)
```

### Example 2: Interactive Session

```bash
python advanced-rag_pipeline.py -i

# Interactive session:
RAG> What is the torque specification for the front shock absorber?
[Detailed answer with metadata]

RAG> history
[Shows query history]

RAG> stats
[Shows session statistics]

RAG> exit
```

### Example 3: Batch Processing

```bash
# Create test queries
cat > test_queries.txt << EOF
What is the torque specification for the front shock absorber?
How to replace the front coil spring?
What are the safety precautions for suspension work?
List all tools required for shock absorber replacement
EOF

# Process batch
python advanced-rag_pipeline.py --batch test_queries.txt --output batch_results.json

# Results saved to batch_results.json with:
# - Query and answer pairs
# - Metadata for each query
# - Timestamps and performance metrics
```

### Example 4: Performance Benchmarking

```bash
python advanced-rag_pipeline.py --benchmark

# Output:
# - Tests 8 predefined queries
# - Shows per-query performance
# - Provides aggregate statistics
# - Identifies performance patterns
```

## Output Formats

### Single Query Output

```
🔍 Processing Query
================================================================================
Query: What is the torque specification for the front shock absorber?

📝 Answer:
----------------------------------------
[Detailed answer from RAG system]

📊 Metadata:
----------------------------------------
Query Type: factual
Chunks Used: 3
Cutoff Reason: score_threshold
Latency: 1250ms
Faithfulness: 0.95
Source Pages: [45, 67, 89]

📚 Retrieved Chunks (3):
----------------------------------------
1. ID: chunk_045_p45_text | Page: 45 | Score: 0.892
2. ID: chunk_067_p67_table | Page: 67 | Score: 0.845
3. ID: chunk_089_p89_text | Page: 89 | Score: 0.798
```

### Batch Results JSON

```json
[
  {
    "query": "What is the torque specification?",
    "answer": "The torque specification for...",
    "query_type": "factual",
    "num_chunks_used": 3,
    "latency_ms": 1250,
    "faithfulness_score": 0.95,
    "timestamp": "2026-06-01T17:30:00"
  }
]
```

## Tips for Effective Usage

### 1. Start with Interactive Mode
- Best for exploration and testing
- Provides immediate feedback
- Tracks session history and statistics

### 2. Use Batch Mode for Systematic Testing
- Create comprehensive test suites
- Compare different query types
- Generate reports for analysis

### 3. Benchmark for Performance Analysis
- Regular performance monitoring
- Identify optimization opportunities
- Track system improvements over time

### 4. Combine with Other Tools
```bash
# Chain with other analysis tools
python advanced-rag_pipeline.py --batch queries.txt --output results.json
python analyze_results.py results.json
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd RAG-Assignment
   python advanced-rag_pipeline.py
   ```

2. **Missing API Keys**
   ```bash
   # Check .env file exists and has correct keys
   cat .env
   ```

3. **No Chunks Found**
   ```bash
   # Ensure preprocessing is complete
   python -m preprocessing.embeddings
   ```

4. **Performance Issues**
   ```bash
   # Use quiet mode for faster processing
   python advanced-rag_pipeline.py --batch queries.txt --quiet
   ```

### Getting Help

```bash
# Show all available options
python advanced-rag_pipeline.py --help

# Interactive help
python advanced-rag_pipeline.py -i
RAG> help
```

---

**Created**: June 1, 2026  
**For**: Ford F-150 Service Manual RAG System  
**Location**: `RAG-Assignment/RAG-Documentation/`