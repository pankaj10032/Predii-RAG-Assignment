---
title: Predii RAG Assignment
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
license: mit
python_version: "3.10"
short_description: Ford F-150 Service Manual RAG System
---

# Ford F-150 Service Manual RAG System

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Pankaj10346/Predii-RAG-Assignment)

🚀 **Live Demo**: [https://huggingface.co/spaces/Pankaj10346/Predii-RAG-Assignment](https://huggingface.co/spaces/Pankaj10346/Predii-RAG-Assignment)

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


## Docker Deployment

### Using Docker

1. **Build the Docker image:**
```bash
docker build -t rag-system .
```

2. **Run the container:**
```bash
docker run -d \
  -p 7860:7860 \
  -e OPENAI_API_KEY=your_openai_key \
  -e COHERE_API_KEY=your_cohere_key \
  -e HF_TOKEN=your_hf_token \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/chunks:/app/chunks \
  --name rag-system \
  rag-system
```

3. **Access the application:**
Open http://localhost:7860 in your browser

### Using Docker Compose (Recommended)

1. **Ensure your `.env` file has all required keys:**
```env
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key
HF_TOKEN=your_hf_token
```

2. **Start the application:**
```bash
docker-compose up -d
```

3. **View logs:**
```bash
docker-compose logs -f
```

4. **Stop the application:**
```bash
docker-compose down
```

### Deploy to Cloud Platforms

#### Deploy to Hugging Face Spaces

1. **Create a new Space on Hugging Face**
2. **Push your code:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/rag-system
git push space main
```

3. **Add secrets in Space settings:**
   - `OPENAI_API_KEY`
   - `COHERE_API_KEY`

#### Deploy to Railway/Render

1. **Connect your GitHub repository**
2. **Set environment variables in the dashboard**
3. **Deploy automatically on push**

#### Deploy to AWS/GCP/Azure

Use the provided Dockerfile to deploy to:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances

Example for Google Cloud Run:
```bash
gcloud run deploy rag-system \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key,COHERE_API_KEY=your_key
```
