# 🏢 Enterprise RAG Features

## Overview

This implementation extends the basic dynamic retrieval RAG with **production-grade enterprise features** based on real-world deployment requirements.

---

## 🔐 1. Access Control & Security

### Role-Based Access Control (RBAC)

**Problem**: RAG systems can leak unauthorized content to users through retrieval.

**Solution**: Security before generation - filter at retrieval time, not after.

```python
class UserContext:
    user_id: str
    roles: List[str]              # ["technician", "engineer"]
    departments: List[str]         # ["service", "engineering"]
    clearance_level: int           # 0=PUBLIC, 1=INTERNAL, 2=CONFIDENTIAL
    tenant_id: str                 # Multi-tenant isolation
```

### Metadata-Based Filtering

Every chunk carries authorization metadata:

```python
class ChunkMetadata:
    sensitivity: SensitivityLevel
    authorized_roles: List[str]
    authorized_departments: List[str]
    has_pii: bool
```

### Pre-Retrieval Filtering

```python
# Build filters BEFORE retrieval
filters = {
    "sensitivity": {"$lte": user.clearance_level},
    "authorized_roles": {"$in": user.roles},
    "tenant_id": user.tenant_id
}

# Apply to vector DB query
results = vector_db.query(
    query_embedding=embedding,
    filters=filters,  # Hard constraint
    top_k=100
)
```

### Key Principles

1. **Security after generation is too late** - LLM has already seen unauthorized content
2. **Metadata travels with chunks** - From ingestion through retrieval
3. **Audit every access** - Who retrieved what, when, and why

---

## 🎨 2. MMR Diversification

### The Problem

At scale, top-k retrieval suffers from:
- **Document-level redundancy**: Multiple chunks from same document
- **Lack of coverage**: Missing diverse perspectives
- **Poor synthesis**: Similar chunks don't help multi-document Q&A

### Maximal Marginal Relevance (MMR)

**Formula**:
```
Score(chunk) = λ · similarity(chunk, query) 
             - (1-λ) · max_similarity(chunk, selected_set)
```

**Parameters**:
- `λ = 0.7`: Balance relevance (70%) vs diversity (30%)
- Higher λ = more relevance, less diversity
- Lower λ = more diversity, less relevance

### Implementation

```python
class MMRDiversifier:
    def select_diverse(
        candidates: List[RetrievalResult],
        query_embedding: List[float],
        k: int,
        lambda_param: float = 0.7
    ) -> List[RetrievalResult]:
        # Iteratively select chunks that are:
        # 1. Highly relevant to query
        # 2. Minimally redundant with selected set
```

### When to Use

✅ **Use MMR when**:
- Summary queries (need diverse perspectives)
- Multi-document Q&A
- Corpus > 10,000 documents
- Synthesis tasks

❌ **Skip MMR when**:
- Factual queries (single answer needed)
- Small corpus (< 1,000 documents)
- Latency is critical

---

## 📊 3. Comprehensive Evaluation

### The Evaluation Trap

**Problem**: Teams overfit to their test set, measuring memorization not generalization.

**Solution**: Multi-layered evaluation with held-out golden dataset.

### Golden Dataset

```python
@dataclass
class GoldenExample:
    query_id: str
    query: str
    query_type: str                    # factual, summary, procedural
    ground_truth_answer: str
    relevant_chunk_ids: List[str]      # For retrieval eval
    difficulty: str                    # easy, medium, hard
    domain: str
```

**Best Practices**:
1. **Hold out from tuning** - Never tune against your eval set
2. **Refresh periodically** - Add real user queries
3. **Stratify by difficulty** - Track performance across complexity
4. **Version control** - Track changes over time

### Evaluation Dimensions

#### 1. Retrieval Quality

```python
# Precision@k: Fraction of retrieved chunks that are relevant
precision = relevant_retrieved / total_retrieved

# Recall@k: Fraction of relevant chunks that were retrieved
recall = relevant_retrieved / total_relevant

# MRR: How high does first relevant chunk rank?
mrr = 1.0 / rank_of_first_relevant

# NDCG: Graded relevance with position discount
```

#### 2. Answer Quality

```python
# Faithfulness: Claims supported by context (anti-hallucination)
faithfulness = supported_claims / total_claims

# Answer Correctness: Match to ground truth
correctness = semantic_similarity(answer, ground_truth)

# Answer Relevance: Addresses the query
relevance = addresses_query(answer, query)
```

#### 3. Citation Quality

```python
# Citation Precision: Cited chunks are in retrieved set
cite_precision = valid_citations / total_citations

# Citation Recall: Relevant chunks are cited
cite_recall = cited_relevant / total_relevant
```

#### 4. System Quality

```python
# Latency breakdown
retrieval_latency_ms
generation_latency_ms
total_latency_ms

# Cost tracking
cost_per_query = (input_tokens * $0.15 + output_tokens * $0.60) / 1M

# Refusal rate
refusal_rate = queries_refused / total_queries
```

### LLM-as-Judge

**Use LLM to evaluate open-ended answers at scale**:

```python
class LLMJudge:
    def evaluate_faithfulness(answer: str, context: str) -> float:
        prompt = f"""
        Context: {context}
        Answer: {answer}
        
        Are all claims in the answer supported by context?
        Score 0.0-1.0
        """
        # Returns score + reasoning
```

**Calibration**:
1. Start with human annotations (100-200 examples)
2. Measure LLM-judge agreement with humans
3. Adjust prompts to improve correlation
4. Periodically re-calibrate with new human labels

---

## 📉 4. Drift Detection

### Types of Drift

#### Data Drift
- Corpus grows or shifts in topic distribution
- New documents semantically different from training data
- **Detection**: Monitor source diversity, topic distribution

#### Embedding Drift
- Model update shifts embedding space
- Old embeddings incompatible with new queries
- **Detection**: Track embedding space statistics (centroid, variance)

#### Query Drift
- Users ask different kinds of questions
- Evaluation set becomes unrepresentative
- **Detection**: Monitor query type distribution

#### Retrieval Drift
- Top-k results gradually degrade
- Precision/recall decline over time
- **Detection**: Weekly evaluation on golden set

### Drift Monitoring

```python
@dataclass
class DriftMetrics:
    timestamp: str
    
    # Retrieval drift
    avg_retrieval_score: float
    retrieval_score_variance: float
    source_diversity: float
    
    # Answer drift
    avg_faithfulness: float
    avg_answer_length: int
    refusal_rate: float
    
    # Performance drift
    avg_latency_ms: float
    p95_latency_ms: float
```

### Drift Response

```python
# Weekly evaluation
metrics = evaluate_on_golden_set()

# Compare to baseline
drift = detect_drift(
    recent_window=metrics[-5:],
    baseline_window=metrics[-10:-5]
)

if drift.retrieval_degradation > 10%:
    alert("Retrieval drift detected")
    # Actions:
    # 1. Re-index corpus
    # 2. Update embeddings
    # 3. Tune retrieval parameters
```

---

## 📝 5. Audit & Governance

### Comprehensive Audit Logs

**Every query produces a durable audit record**:

```python
@dataclass
class AuditLog:
    timestamp: str
    session_id: str
    user_id: str
    user_roles: List[str]
    
    # Query
    query: str
    query_hash: str                    # Privacy-preserving
    
    # Retrieval
    filters_applied: Dict
    retrieved_doc_ids: List[str]
    num_chunks_retrieved: int
    num_chunks_used: int
    
    # Generation
    answer_generated: bool
    answer_hash: str
    citations: List[str]
    
    # Quality
    faithfulness_score: float
    pii_detected: bool
    access_violations: List[str]
    
    # Performance
    latency_ms: float
    tokens_used: int
    cost_usd: float
    model: str
```

### Why Audit Logs Matter

1. **Compliance**: SOC 2, HIPAA, GDPR requirements
2. **Security**: Detect unauthorized access attempts
3. **Debugging**: Trace answers back to source documents
4. **Analytics**: Understand usage patterns
5. **Trust**: Demonstrate responsible AI use

### Data Lineage

**Trace every answer back to source documents**:

```
User Query
    ↓
Audit Log Entry (timestamp, user, query_hash)
    ↓
Retrieved Chunks (doc_ids, scores)
    ↓
Generated Answer (answer_hash, citations)
    ↓
Source Documents (original PDFs, pages)
```

### PII Handling

```python
# At ingestion
pii_detected = detect_pii(chunk.content)
chunk.metadata.has_pii = pii_detected
chunk.metadata.sensitivity = CONFIDENTIAL if pii_detected else INTERNAL

# At retrieval
if chunk.metadata.has_pii:
    # Apply stricter access control
    # Log PII access
    # Redact if necessary

# At generation
if detect_pii(answer):
    alert("PII in answer")
    # Redact or refuse
```

---

## 🎯 6. Production Architecture

### Complete Enterprise Stack

```
[Data Sources]
    ↓
[Ingestion Pipeline]
  - Layout-aware parsing
  - PII detection
  - Metadata enrichment
  - Semantic chunking
  - Embedding generation (versioned)
    ↓
[Vector DB + Metadata]
  - Chunks with rich metadata
  - Access control attributes
  - Version-tracked embeddings
    ↓
[Query Pipeline]
  - Identity resolution
  - Metadata pre-filtering
  - Hybrid retrieval (dense + sparse)
  - MMR diversification
  - Reranking
  - Dynamic cutoff
    ↓
[LLM Generation]
  - Citation-aware prompt
  - Confidence gating
    ↓
[Audit & Monitoring]
  - Audit logs
  - Metrics emission
  - Drift detection
  - Compliance reporting
```

### Key Design Decisions

#### 1. Shared Index vs Partitioned

**Shared Index with Metadata Filtering**:
- ✅ Simpler to maintain
- ✅ Better resource utilization
- ❌ Risk if filters misconfigured
- ❌ Potential cross-tenant leakage

**Partitioned Indexes by Tenant**:
- ✅ Stronger isolation
- ✅ Better for regulated industries
- ❌ Higher operational complexity
- ❌ More infrastructure cost

**Recommendation**: Partitioned for multi-tenant SaaS, shared for single-tenant enterprise.

#### 2. Embedding Model Selection

**Considerations**:
- **Domain specificity**: General vs specialized (legal, medical, code)
- **Multilingual**: Required for multi-language corpora
- **Dimensionality**: Quality vs cost trade-off
- **Matryoshka embeddings**: Truncate at inference time

**Versioning**:
```python
chunk.metadata.embedding_model = "text-embedding-3-large"
chunk.metadata.embedding_version = "1.0"

# When upgrading:
# 1. Version new embeddings
# 2. Re-embed full corpus
# 3. A/B test before cutover
```

#### 3. Cost Optimization

**Do cheap filtering early, expensive LLM calls last**:

```python
# Cheap → Expensive pipeline
Metadata filter (free)
    ↓
ANN search (cheap)
    ↓
BM25 search (cheap)
    ↓
RRF fusion (cheap)
    ↓
MMR diversification (cheap)
    ↓
Reranking (moderate)
    ↓
LLM generation (expensive)
```

**Caching Strategy**:
- Cache query embeddings (frequent queries)
- Cache retrieval results (identical queries)
- Cache reranker results (similar queries)
- Precompute embeddings at ingestion (never at query time)

---

## 📈 7. Monitoring & Alerts

### Metrics to Track

#### Retrieval Layer
```python
# Real-time metrics
retrieval_latency_p50
retrieval_latency_p95
retrieval_latency_p99

# Quality metrics (from evaluation)
precision_at_k
recall_at_k
source_diversity

# Drift indicators
avg_retrieval_score_7d
retrieval_score_variance_7d
```

#### Generation Layer
```python
# Quality metrics
faithfulness_score
citation_accuracy
refusal_rate

# Performance
generation_latency_p95
tokens_per_query
cost_per_query
```

#### System Health
```python
# Availability
uptime_percentage
error_rate

# Resource utilization
vector_db_query_rate
embedding_api_rate_limit
llm_api_rate_limit
```

### Alert Thresholds

```python
# Critical alerts
if faithfulness_score < 0.70:
    alert("CRITICAL: High hallucination rate")

if pii_leakage_detected:
    alert("CRITICAL: PII in answer")

if access_violation:
    alert("CRITICAL: Unauthorized access")

# Warning alerts
if retrieval_score_degradation > 10%:
    alert("WARNING: Retrieval drift detected")

if p95_latency > 5000ms:
    alert("WARNING: High latency")

if cost_per_query > $0.50:
    alert("WARNING: High cost")
```

---

## 🔒 8. Compliance Frameworks

### SOC 2 Requirements

✅ **Access Control**: RBAC with audit logs
✅ **Data Encryption**: At rest and in transit
✅ **Audit Trails**: Comprehensive logging
✅ **Monitoring**: Real-time alerts
✅ **Incident Response**: Automated detection

### HIPAA Requirements

✅ **PHI Protection**: PII detection and redaction
✅ **Access Logs**: Who accessed what PHI
✅ **Encryption**: AES-256 for PHI
✅ **Audit Controls**: Tamper-proof logs
✅ **Data Retention**: Configurable retention policies

### GDPR Requirements

✅ **Right to Access**: User can query their data
✅ **Right to Deletion**: Remove user data from corpus
✅ **Data Minimization**: Only retrieve necessary chunks
✅ **Purpose Limitation**: Log query purpose
✅ **Consent Management**: Track user consent

---

## 🎓 Implementation Checklist

### Phase 1: Foundation (Week 1-2)
- [ ] Implement metadata schema
- [ ] Add access control filters
- [ ] Set up audit logging
- [ ] Create golden dataset (50 examples)

### Phase 2: Quality (Week 3-4)
- [ ] Implement MMR diversification
- [ ] Add LLM-as-judge evaluation
- [ ] Set up drift detection
- [ ] Configure monitoring dashboards

### Phase 3: Security (Week 5-6)
- [ ] Implement PII detection
- [ ] Add role-based access control
- [ ] Set up compliance reporting
- [ ] Conduct security audit

### Phase 4: Optimization (Week 7-8)
- [ ] Implement caching strategy
- [ ] Optimize retrieval pipeline
- [ ] Tune cost/quality trade-offs
- [ ] Load testing and scaling

---

## 📚 Key Takeaways

1. **Security before generation** - Filter at retrieval, not after
2. **Metadata is infrastructure** - Not an afterthought
3. **Evaluation is continuous** - Not a one-time milestone
4. **Drift is inevitable** - Monitor and respond
5. **Audit everything** - Compliance and trust
6. **Cost optimization early** - Cheap filters before expensive LLM calls
7. **Golden dataset is sacred** - Never tune against it

---

## 🔗 Related Files

- **Implementation**: `enterprise_rag_pipeline.py`
- **Evaluation**: `evaluation_framework.py`
- **Basic RAG**: `advanced_rag_pipeline.py`
- **Benchmarking**: `benchmark_rag.py`

---

**Enterprise RAG is not a product — it's an engineering discipline.**

*The gap between a demo and a system that earns trust at scale is filled with decisions about access control, evaluation rigor, drift management, and governance.*
