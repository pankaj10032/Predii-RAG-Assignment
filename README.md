---
title: Predii RAG Assignment
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
python_version: "3.10"
short_description: Ford F-150 Service Manual RAG System
---

# Ford F-150 Service Manual RAG System

A production-ready Retrieval-Augmented Generation (RAG) system for querying Ford F-150 service manual information.

## Features

- **Query Rewriting**: Step-back prompting for better retrieval
- **Hybrid Search**: Dense (vector) + Sparse (BM25) retrieval
- **Cohere Reranking**: Precision ranking of results
- **Dynamic Chunk Selection**: 1-20 chunks based on query complexity
- **MMR Diversification**: Reduced redundancy in results
- **Faithfulness Evaluation**: Quality assurance using LLM-as-judge
- **Comprehensive Audit Logging**: Track all queries and responses

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key
- Cohere API Key (optional, for reranking)

### Installation

```bash
pip install -r requirements.txt
```

### Setup

1. Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
```

2. Preprocess the PDF (first time only):
```bash
python -m preprocessing.embeddings
```

3. Run the web interface:
```bash
python app.py
```

4. Or run the CLI:
```bash
python unified_rag_system.py
```

## Usage

### Web Interface

The Gradio interface provides a user-friendly way to interact with the RAG system:

- Ask questions about Ford F-150 suspension and repair
- Toggle query rewriting, MMR diversification, and evaluation
- View retrieved chunks and evaluation metrics

### CLI

Run queries from the command line:

```python
from unified_rag_system import UnifiedRAGSystem

rag = UnifiedRAGSystem()
result = rag.query("What is the torque specification for the front shock absorber?")
print(result.answer)
```

## Project Structure

```
RAG-Assignment/
├── preprocessing/      # PDF processing and chunking
├── retrieval/          # Retrieval and generation
├── reranking/          # Reranking and diversification
├── utils/              # Shared utilities
├── chunks/             # Document chunks
├── chroma_db/          # Vector database
├── tests/              # Test files
├── app.py              # Gradio web interface
├── unified_rag_system.py
├── requirements.txt
└── .env
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system architecture.

## Requirements

See [requirements.txt](requirements.txt) for dependencies.

## License

MIT License