"""
RAG Evaluation Framework
Implements: Golden dataset, LLM-as-judge, Human calibration, Drift detection
"""

import json
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import statistics

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


# ========================= DATA MODELS =========================
@dataclass
class GoldenExample:
    """Single evaluation example"""
    query_id: str
    query: str
    query_type: str  # factual, summary, procedural
    ground_truth_answer: str
    relevant_chunk_ids: List[str]
    difficulty: str  # easy, medium, hard
    domain: str
    created_date: str
    last_updated: str


@dataclass
class EvaluationResult:
    """Single query evaluation result"""
    query_id: str
    query: str
    retrieved_chunks: List[str]
    generated_answer: str
    
    # Retrieval metrics
    precision: float
    recall: float
    mrr: float
    
    # Answer quality
    faithfulness: float
    answer_correctness: float
    answer_relevance: float
    
    # Citations
    citation_precision: float
    citation_recall: float
    
    # Latency
    retrieval_latency_ms: float
    generation_latency_ms: float
    total_latency_ms: float
    
    # Cost
    cost_usd: float
    
    timestamp: str


@dataclass
class DriftMetrics:
    """Track system drift over time"""
    timestamp: str
    
    # Retrieval drift
    avg_retrieval_score: float
    retrieval_score_variance: float
    source_diversity: float  # Unique docs / total chunks
    
    # Answer drift
    avg_faithfulness: float
    avg_answer_length: int
    refusal_rate: float
    
    # Performance drift
    avg_latency_ms: float
    p95_latency_ms: float
    avg_cost_usd: float


# ========================= GOLDEN DATASET =========================
class GoldenDataset:
    """Manage golden evaluation dataset"""
    
    def __init__(self, dataset_file: str = "golden_dataset.json"):
        self.dataset_file = dataset_file
        self.examples: List[GoldenExample] = []
        self.load()
    
    def load(self):
        """Load golden dataset"""
        try:
            with open(self.dataset_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.examples = [GoldenExample(**ex) for ex in data]
            print(f"✅ Loaded {len(self.examples)} golden examples")
        except FileNotFoundError:
            print(f"⚠️  No golden dataset found, creating sample...")
            self._create_sample_dataset()
    
    def _create_sample_dataset(self):
        """Create sample golden dataset"""
        self.examples = [
            GoldenExample(
                query_id="q001",
                query="What is the torque specification for the front shock absorber?",
                query_type="factual",
                ground_truth_answer="The torque specification for the front shock absorber is 350 Nm (258 lb-ft).",
                relevant_chunk_ids=["chunk_42"],
                difficulty="easy",
                domain="suspension",
                created_date="2024-01-01",
                last_updated="2024-01-01"
            ),
            GoldenExample(
                query_id="q002",
                query="Summarize all suspension inspection procedures",
                query_type="summary",
                ground_truth_answer="Suspension inspection includes: visual inspection, ball joint testing, shock absorber evaluation, ride height measurement, and alignment checks.",
                relevant_chunk_ids=["chunk_5", "chunk_12", "chunk_18", "chunk_25", "chunk_31"],
                difficulty="medium",
                domain="suspension",
                created_date="2024-01-01",
                last_updated="2024-01-01"
            ),
            GoldenExample(
                query_id="q003",
                query="How do I replace the front coil spring?",
                query_type="procedural",
                ground_truth_answer="To replace the front coil spring: 1) Raise vehicle, 2) Remove wheel, 3) Compress spring, 4) Remove mounting bolts, 5) Install new spring, 6) Torque to spec.",
                relevant_chunk_ids=["chunk_67", "chunk_68", "chunk_69"],
                difficulty="medium",
                domain="suspension",
                created_date="2024-01-01",
                last_updated="2024-01-01"
            )
        ]
        self.save()
    
    def save(self):
        """Save golden dataset"""
        with open(self.dataset_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(ex) for ex in self.examples], f, indent=2)
        print(f"💾 Saved {len(self.examples)} golden examples")
    
    def add_example(self, example: GoldenExample):
        """Add new example to dataset"""
        self.examples.append(example)
        self.save()
    
    def get_by_type(self, query_type: str) -> List[GoldenExample]:
        """Get examples by query type"""
        return [ex for ex in self.examples if ex.query_type == query_type]
    
    def get_by_difficulty(self, difficulty: str) -> List[GoldenExample]:
        """Get examples by difficulty"""
        return [ex for ex in self.examples if ex.difficulty == difficulty]


# ========================= LLM-AS-JUDGE =========================
class LLMJudge:
    """Use LLM to evaluate answer quality"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
    
    def evaluate_faithfulness(self, answer: str, context: str) -> Tuple[float, str]:
        """
        Evaluate if answer is faithful to context
        Returns: (score, reasoning)
        """
        prompt = f"""You are evaluating answer faithfulness.

Context:
{context}

Answer:
{answer}

Task: Evaluate if every claim in the answer is supported by the context.

Output JSON:
{{
  "score": <0.0 to 1.0>,
  "reasoning": "<brief explanation>",
  "unsupported_claims": ["<claim 1>", "<claim 2>"]
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return result.get("score", 0.0), result.get("reasoning", "")
        except Exception as e:
            return 0.0, f"Error: {e}"
    
    def evaluate_answer_correctness(
        self,
        answer: str,
        ground_truth: str,
        context: str
    ) -> Tuple[float, str]:
        """
        Evaluate answer correctness against ground truth
        Returns: (score, reasoning)
        """
        prompt = f"""You are evaluating answer correctness.

Ground Truth Answer:
{ground_truth}

Generated Answer:
{answer}

Context:
{context}

Task: Evaluate if the generated answer is correct compared to ground truth.
Consider semantic equivalence, not just exact matching.

Output JSON:
{{
  "score": <0.0 to 1.0>,
  "reasoning": "<brief explanation>",
  "key_differences": ["<difference 1>", "<difference 2>"]
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return result.get("score", 0.0), result.get("reasoning", "")
        except Exception as e:
            return 0.0, f"Error: {e}"
    
    def evaluate_answer_relevance(self, answer: str, query: str) -> Tuple[float, str]:
        """
        Evaluate if answer is relevant to query
        Returns: (score, reasoning)
        """
        prompt = f"""You are evaluating answer relevance.

Query:
{query}

Answer:
{answer}

Task: Evaluate if the answer directly addresses the query.

Output JSON:
{{
  "score": <0.0 to 1.0>,
  "reasoning": "<brief explanation>"
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return result.get("score", 0.0), result.get("reasoning", "")
        except Exception as e:
            return 0.0, f"Error: {e}"


# ========================= EVALUATION RUNNER =========================
class EvaluationRunner:
    """Run comprehensive RAG evaluation"""
    
    def __init__(self, rag_pipeline, golden_dataset: GoldenDataset):
        self.rag_pipeline = rag_pipeline
        self.golden_dataset = golden_dataset
        self.judge = LLMJudge()
        self.results: List[EvaluationResult] = []
    
    def evaluate_retrieval(
        self,
        retrieved_ids: List[str],
        relevant_ids: List[str]
    ) -> Tuple[float, float, float]:
        """
        Compute retrieval metrics
        Returns: (precision, recall, mrr)
        """
        retrieved_set = set(retrieved_ids)
        relevant_set = set(relevant_ids)
        
        # Precision
        if retrieved_set:
            precision = len(retrieved_set.intersection(relevant_set)) / len(retrieved_set)
        else:
            precision = 0.0
        
        # Recall
        if relevant_set:
            recall = len(retrieved_set.intersection(relevant_set)) / len(relevant_set)
        else:
            recall = 0.0
        
        # MRR (Mean Reciprocal Rank)
        mrr = 0.0
        for rank, chunk_id in enumerate(retrieved_ids, 1):
            if chunk_id in relevant_set:
                mrr = 1.0 / rank
                break
        
        return precision, recall, mrr
    
    def evaluate_citations(
        self,
        citations: List[str],
        retrieved_ids: List[str],
        relevant_ids: List[str]
    ) -> Tuple[float, float]:
        """
        Evaluate citation quality
        Returns: (precision, recall)
        """
        citation_set = set(citations)
        retrieved_set = set(retrieved_ids)
        relevant_set = set(relevant_ids)
        
        # Citation precision: cited chunks should be in retrieved set
        if citation_set:
            precision = len(citation_set.intersection(retrieved_set)) / len(citation_set)
        else:
            precision = 0.0
        
        # Citation recall: relevant chunks should be cited
        if relevant_set:
            recall = len(citation_set.intersection(relevant_set)) / len(relevant_set)
        else:
            recall = 0.0
        
        return precision, recall
    
    def run_evaluation(self, verbose: bool = True) -> Dict:
        """Run evaluation on golden dataset"""
        
        print("=" * 80)
        print("🧪 Running RAG Evaluation")
        print("=" * 80)
        print(f"Golden examples: {len(self.golden_dataset.examples)}")
        print()
        
        self.results = []
        
        for i, example in enumerate(self.golden_dataset.examples, 1):
            if verbose:
                print(f"[{i}/{len(self.golden_dataset.examples)}] {example.query_id}: {example.query[:60]}...")
            
            # Run query
            start_time = time.time()
            
            try:
                # Assuming rag_pipeline has a query method
                result = self.rag_pipeline.query(example.query, verbose=False)
                
                retrieval_time = time.time()
                
                # Extract data
                retrieved_ids = [c['id'] for c in result.get('chunks', [])]
                answer = result.get('answer', '')
                citations = result.get('citations', [])
                context = "\n".join([c.get('content', '') for c in result.get('chunks', [])])
                
                generation_time = time.time()
                
                # Evaluate retrieval
                precision, recall, mrr = self.evaluate_retrieval(
                    retrieved_ids,
                    example.relevant_chunk_ids
                )
                
                # Evaluate answer quality
                faithfulness, _ = self.judge.evaluate_faithfulness(answer, context)
                correctness, _ = self.judge.evaluate_answer_correctness(
                    answer,
                    example.ground_truth_answer,
                    context
                )
                relevance, _ = self.judge.evaluate_answer_relevance(answer, example.query)
                
                # Evaluate citations
                cite_precision, cite_recall = self.evaluate_citations(
                    citations,
                    retrieved_ids,
                    example.relevant_chunk_ids
                )
                
                # Create result
                eval_result = EvaluationResult(
                    query_id=example.query_id,
                    query=example.query,
                    retrieved_chunks=retrieved_ids,
                    generated_answer=answer,
                    precision=precision,
                    recall=recall,
                    mrr=mrr,
                    faithfulness=faithfulness,
                    answer_correctness=correctness,
                    answer_relevance=relevance,
                    citation_precision=cite_precision,
                    citation_recall=cite_recall,
                    retrieval_latency_ms=(retrieval_time - start_time) * 1000,
                    generation_latency_ms=(generation_time - retrieval_time) * 1000,
                    total_latency_ms=(generation_time - start_time) * 1000,
                    cost_usd=result.get('cost', 0.0),
                    timestamp=datetime.now().isoformat()
                )
                
                self.results.append(eval_result)
                
                if verbose:
                    print(f"   ✓ P={precision:.2f} R={recall:.2f} F={faithfulness:.2f} C={correctness:.2f}")
            
            except Exception as e:
                if verbose:
                    print(f"   ✗ Error: {e}")
        
        # Compute aggregate metrics
        return self._compute_aggregate_metrics()
    
    def _compute_aggregate_metrics(self) -> Dict:
        """Compute aggregate metrics across all results"""
        
        if not self.results:
            return {}
        
        metrics = {
            "total_queries": len(self.results),
            "retrieval": {
                "avg_precision": statistics.mean([r.precision for r in self.results]),
                "avg_recall": statistics.mean([r.recall for r in self.results]),
                "avg_mrr": statistics.mean([r.mrr for r in self.results]),
            },
            "answer_quality": {
                "avg_faithfulness": statistics.mean([r.faithfulness for r in self.results]),
                "avg_correctness": statistics.mean([r.answer_correctness for r in self.results]),
                "avg_relevance": statistics.mean([r.answer_relevance for r in self.results]),
            },
            "citations": {
                "avg_precision": statistics.mean([r.citation_precision for r in self.results]),
                "avg_recall": statistics.mean([r.citation_recall for r in self.results]),
            },
            "performance": {
                "avg_latency_ms": statistics.mean([r.total_latency_ms for r in self.results]),
                "p95_latency_ms": statistics.quantiles([r.total_latency_ms for r in self.results], n=20)[18] if len(self.results) > 1 else 0,
                "avg_cost_usd": statistics.mean([r.cost_usd for r in self.results]),
            }
        }
        
        return metrics
    
    def print_report(self, metrics: Dict):
        """Print evaluation report"""
        
        print("\n" + "=" * 80)
        print("📊 EVALUATION REPORT")
        print("=" * 80)
        
        print(f"\n📈 Retrieval Metrics:")
        print(f"   Precision@k: {metrics['retrieval']['avg_precision']:.3f}")
        print(f"   Recall@k:    {metrics['retrieval']['avg_recall']:.3f}")
        print(f"   MRR:         {metrics['retrieval']['avg_mrr']:.3f}")
        
        print(f"\n💬 Answer Quality:")
        print(f"   Faithfulness: {metrics['answer_quality']['avg_faithfulness']:.3f}")
        print(f"   Correctness:  {metrics['answer_quality']['avg_correctness']:.3f}")
        print(f"   Relevance:    {metrics['answer_quality']['avg_relevance']:.3f}")
        
        print(f"\n📝 Citations:")
        print(f"   Precision: {metrics['citations']['avg_precision']:.3f}")
        print(f"   Recall:    {metrics['citations']['avg_recall']:.3f}")
        
        print(f"\n⚡ Performance:")
        print(f"   Avg Latency: {metrics['performance']['avg_latency_ms']:.0f}ms")
        print(f"   P95 Latency: {metrics['performance']['p95_latency_ms']:.0f}ms")
        print(f"   Avg Cost:    ${metrics['performance']['avg_cost_usd']:.4f}")
        
        print("\n" + "=" * 80)
    
    def save_results(self, filename: str = "evaluation_results.json"):
        """Save evaluation results"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "results": [asdict(r) for r in self.results],
            "aggregate_metrics": self._compute_aggregate_metrics()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")


# ========================= DRIFT DETECTION =========================
class DriftDetector:
    """Detect system drift over time"""
    
    def __init__(self, history_file: str = "drift_history.jsonl"):
        self.history_file = history_file
        self.history: List[DriftMetrics] = []
        self.load_history()
    
    def load_history(self):
        """Load drift history"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    self.history.append(DriftMetrics(**json.loads(line)))
            print(f"✅ Loaded {len(self.history)} drift snapshots")
        except FileNotFoundError:
            print("⚠️  No drift history found")
    
    def record_snapshot(self, evaluation_results: List[EvaluationResult]):
        """Record current system state"""
        
        if not evaluation_results:
            return
        
        # Compute metrics
        retrieval_scores = [r.precision for r in evaluation_results]
        
        snapshot = DriftMetrics(
            timestamp=datetime.now().isoformat(),
            avg_retrieval_score=statistics.mean(retrieval_scores),
            retrieval_score_variance=statistics.variance(retrieval_scores) if len(retrieval_scores) > 1 else 0.0,
            source_diversity=len(set([c for r in evaluation_results for c in r.retrieved_chunks])) / sum([len(r.retrieved_chunks) for r in evaluation_results]),
            avg_faithfulness=statistics.mean([r.faithfulness for r in evaluation_results]),
            avg_answer_length=statistics.mean([len(r.generated_answer.split()) for r in evaluation_results]),
            refusal_rate=sum([1 for r in evaluation_results if "don't have" in r.generated_answer.lower()]) / len(evaluation_results),
            avg_latency_ms=statistics.mean([r.total_latency_ms for r in evaluation_results]),
            p95_latency_ms=statistics.quantiles([r.total_latency_ms for r in evaluation_results], n=20)[18] if len(evaluation_results) > 1 else 0,
            avg_cost_usd=statistics.mean([r.cost_usd for r in evaluation_results])
        )
        
        self.history.append(snapshot)
        
        # Save
        with open(self.history_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(snapshot)) + '\n')
        
        print(f"📸 Drift snapshot recorded")
    
    def detect_drift(self, window_size: int = 5) -> Dict:
        """Detect drift by comparing recent vs historical performance"""
        
        if len(self.history) < window_size * 2:
            return {"drift_detected": False, "reason": "Insufficient history"}
        
        # Compare recent window vs baseline
        recent = self.history[-window_size:]
        baseline = self.history[-window_size*2:-window_size]
        
        recent_retrieval = statistics.mean([s.avg_retrieval_score for s in recent])
        baseline_retrieval = statistics.mean([s.avg_retrieval_score for s in baseline])
        
        recent_faithfulness = statistics.mean([s.avg_faithfulness for s in recent])
        baseline_faithfulness = statistics.mean([s.avg_faithfulness for s in baseline])
        
        # Detect significant degradation (>10%)
        retrieval_drift = (baseline_retrieval - recent_retrieval) / baseline_retrieval
        faithfulness_drift = (baseline_faithfulness - recent_faithfulness) / baseline_faithfulness
        
        drift_detected = retrieval_drift > 0.10 or faithfulness_drift > 0.10
        
        return {
            "drift_detected": drift_detected,
            "retrieval_drift_pct": retrieval_drift * 100,
            "faithfulness_drift_pct": faithfulness_drift * 100,
            "recent_retrieval": recent_retrieval,
            "baseline_retrieval": baseline_retrieval,
            "recent_faithfulness": recent_faithfulness,
            "baseline_faithfulness": baseline_faithfulness
        }


# ========================= MAIN =========================
def main():
    """Run evaluation framework"""
    
    # Load golden dataset
    golden_dataset = GoldenDataset()
    
    # Initialize RAG pipeline (would use actual pipeline)
    print("\n⚠️  Note: Using mock pipeline for demo")
    print("   In production, pass your actual RAG pipeline\n")
    
    # Mock pipeline for demo
    class MockRAGPipeline:
        def query(self, query: str, verbose: bool = False):
            return {
                "answer": "Mock answer for: " + query,
                "chunks": [{"id": "chunk_1", "content": "Mock content"}],
                "citations": ["chunk_1"],
                "cost": 0.001
            }
    
    mock_pipeline = MockRAGPipeline()
    
    # Run evaluation
    runner = EvaluationRunner(mock_pipeline, golden_dataset)
    metrics = runner.run_evaluation(verbose=True)
    runner.print_report(metrics)
    runner.save_results()
    
    # Drift detection
    drift_detector = DriftDetector()
    drift_detector.record_snapshot(runner.results)
    drift_report = drift_detector.detect_drift()
    
    print("\n" + "=" * 80)
    print("📉 DRIFT DETECTION")
    print("=" * 80)
    print(f"Drift Detected: {drift_report.get('drift_detected', False)}")
    if drift_report.get('drift_detected'):
        print(f"Retrieval Drift: {drift_report.get('retrieval_drift_pct', 0):.1f}%")
        print(f"Faithfulness Drift: {drift_report.get('faithfulness_drift_pct', 0):.1f}%")


if __name__ == "__main__":
    main()
