from typing import List, Tuple
from utils.data_models import RetrievalResult
from utils.config import Config


class DynamicCutoff:
    """Score-based dynamic chunk selection"""
    
    @staticmethod
    def determine_cutoff(results: List[RetrievalResult], expected_chunks: int) -> Tuple[List[RetrievalResult], str]:
        """
        Apply dynamic cutoff logic
        
        Args:
            results: Reranked results
            expected_chunks: Expected number of chunks based on query type
            
        Returns:
            Tuple of (selected chunks, cutoff reason)
        """
        if not results:
            return [], "No results"
        
        scores = [r.score for r in results]
        
        if scores[0] >= Config.CLEAR_WINNER_SCORE:
            if len(scores) > 1 and (scores[0] - scores[1]) >= Config.CLEAR_WINNER_GAP:
                return results[:1], f"Clear winner (score={scores[0]:.3f}, gap={scores[0]-scores[1]:.3f})"
        
        if len(scores) > 1 and scores[1] >= 0.85:
            if len(scores) > 2 and (scores[1] - scores[2]) >= 0.15:
                return results[:2], f"Strong pair (scores={scores[0]:.3f}, {scores[1]:.3f})"
        
        for i in range(1, min(len(scores), Config.MAX_CHUNKS)):
            gap = scores[i-1] - scores[i]
            if gap >= Config.NATURAL_GAP_THRESHOLD:
                return results[:i], f"Natural gap at position {i} (gap={gap:.3f})"
        
        cutoff = min(expected_chunks, len(results))
        return results[:cutoff], f"Query-type default ({expected_chunks} chunks)"
