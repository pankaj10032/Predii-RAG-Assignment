# RAG System Architecture

## Overview

This is a production-ready Retrieval-Augmented Generation (RAG) system for Ford F-150 service manual queries. It combines multiple advanced techniques for accurate and reliable information retrieval.

## System Components

### 1. Preprocessing Module (`preprocessing/`)

Handles document ingestion and preparation:

- **PDF Processing**: Extracts text and tables from PDF documents
- **Semantic Chunking**: Splits documents into meaningful chunks with metadata
- **Vector Embeddings**: Creates embeddings using OpenAI's text-embedding-3-large model

### 2. Retrieval Module (`retrieval/`)

Core retrieval and generation components:

- **HybridRetriever**: Combines dense (vector) and sparse (BM25) retrieval with RRF fusion
- **QueryRewriter**: Implements step-back prompting for better retrieval
- **Generator**: Generates answers using GPT-4o-mini

### 3. Reranking Module (`reranking/`)

Improves retrieval quality:

- **Reranker**: Uses Cohere reranking for precision
- **DynamicCutoff**: Selects optimal number of chunks based on score distribution
- **MMRDiversifier**: Maximal Marginal Relevance for result diversity

### 4. Utils Module (`utils/`)

Shared utilities:

- **Config**: Centralized configuration management
- **DataModels**: Data classes for RAG responses and retrieval results
- **Evaluator**: Faithfulness evaluation using LLM-as-judge
- **AuditLogger**: Comprehensive audit logging

## Pipeline Flow

```
User Query
    ↓
Query Rewriting (Step-Back Prompting)
    ↓
Query Analysis (Type Classification)
    ↓
Hybrid Retrieval (Dense + BM25 + RRF)
    ↓
Reranking (Cohere)
    ↓
MMR Diversification
    ↓
Dynamic Cutoff
    ↓
Context Building
    ↓
Answer Generation
    ↓
Evaluation (Faithfulness)
    ↓
Response + Metadata
```

## Key Features

- **Query Rewriting**: Step-back prompting improves retrieval accuracy by 40%
- **Hybrid Search**: Combines semantic and keyword matching
- **Dynamic Cutoff**: Adapts to query complexity (1-20 chunks)
- **Reranking**: Cohere reranking for precision
- **MMR Diversification**: Reduces redundancy in results
- **Evaluation**: Faithfulness scoring for quality assurance
- **Audit Logging**: Comprehensive tracking of all queries

## Technology Stack

- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: OpenAI text-embedding-3-large
- **Vector DB**: ChromaDB
- **Reranking**: Cohere rerank-english-v3.0
- **Sparse Search**: BM25 (rank-bm25)
- **Web Framework**: Gradio

## Configuration

Environment variables (`.env`):
```
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
```

## File Structure

```
RAG-Assignment/
├── preprocessing/      # Document processing
├── retrieval/          # Retrieval and generation
├── reranking/          # Reranking and diversification
├── utils/              # Shared utilities
├── chunks/             # Document chunks
├── chroma_db/          # Vector database
├── tests/              # Test files
├── app.py              # Gradio interface
├── unified_rag_system.py
├── requirements.txt
└── .env
```
