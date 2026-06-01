"""Audit logging for RAG system"""

import json
import hashlib
from typing import Dict


class AuditLogger:
    """Comprehensive audit logging for queries and responses"""
    
    def __init__(self, log_file: str = "audit_logs.jsonl"):
        """Initialize audit logger with log file path"""
        self.log_file = log_file
    
    def log(self, entry: Dict):
        """
        Write audit entry to log file
        
        Args:
            entry: Dictionary containing audit information
        """
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    
    @staticmethod
    def hash_text(text: str) -> str:
        """
        Hash text for privacy-preserving logging
        
        Args:
            text: Text to hash
            
        Returns:
            First 16 characters of SHA256 hash
        """
        return hashlib.sha256(text.encode()).hexdigest()[:16]
