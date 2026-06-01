"""Data models for RAG system"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class QueryType(Enum):
    """Query classification types"""
    FACTUAL = "factual"
    MULTI_HOP = "multi_hop"
    TEMPORAL = "temporal"
    COMPARISON = "comparison"
    PROCEDURAL = "procedural"
    SUMMARY = "summary"
    OUT_OF_SCOPE = "out_of_scope"


@dataclass
class RetrievalResult:
    """Single retrieval result with metadata"""
    chunk_id: str
    content: str
    score: float
    page: int
    rank: int


@dataclass
class RAGResponse:
    """Complete RAG response with all metadata"""
    query: str
    answer: str
    query_type: str
    num_chunks_used: int
    chunks: List[Dict]
    cutoff_reason: str
    latency_ms: float
    query_rewritten: bool = False
    retrieval_query: str = ""
    faithfulness_score: Optional[float] = None
    citation_accuracy: Optional[float] = None
    session_id: str = ""
    timestamp: str = ""
