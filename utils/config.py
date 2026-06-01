"""Configuration settings for RAG system"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Centralized configuration for RAG system"""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
    
    COLLECTION_NAME = "ford_f150_suspension"
    CHUNKS_JSON = "chunks/suspension_chunks_final.json"
    CHROMA_PATH = "chroma_db"
    
    INITIAL_CANDIDATES = 100
    RERANK_TOP_K = 50
    MIN_CHUNKS = 1
    MAX_CHUNKS = 20
    
    CLEAR_WINNER_SCORE = 0.92
    CLEAR_WINNER_GAP = 0.20
    NATURAL_GAP_THRESHOLD = 0.15
    
    FACTUAL_DEFAULT = 3
    SUMMARY_DEFAULT = 12
    PROCEDURAL_DEFAULT = 8
    
    MMR_LAMBDA = 0.7
    
    LLM_MODEL = "gpt-4o-mini"
    LLM_TEMPERATURE = 0.1
    LLM_MAX_TOKENS = 800
    
    ENABLE_QUERY_REWRITING = True
    ENABLE_MMR = True
    ENABLE_EVALUATION = True
    ENABLE_AUDIT = True
