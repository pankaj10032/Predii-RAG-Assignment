from typing import List
from utils.data_models import RetrievalResult
from utils.config import Config


class MMRDiversifier:
    """Maximal Marginal Relevance for result diversification"""
    
    @staticmethod
    def diversify(candidates: List[RetrievalResult], k: int, lambda_param: float = Config.MMR_LAMBDA) -> List[RetrievalResult]:
        """
        Select diverse chunks using MMR
        
        Args:
            candidates: Candidate results
            k: Number of results to select
            lambda_param: Balance between relevance and diversity
            
        Returns:
            Diversified results
        """
        if len(candidates) <= k:
            return candidates
        
        selected = [candidates[0]]
        remaining = candidates[1:]
        
        while len(selected) < k and remaining:
            best_score = float('-inf')
            best_idx = 0
            
            for idx, candidate in enumerate(remaining):
                relevance = candidate.score
                
                max_sim = max([0.5 if sel.page == candidate.page else 0.1 for sel in selected])
                
                mmr_score = lambda_param * relevance - (1 - lambda_param) * max_sim
                
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = idx
            
            selected.append(remaining.pop(best_idx))
        
        return selected
