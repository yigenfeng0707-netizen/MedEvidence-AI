"""
MedEvidence AI - 医学循证智能检索助手
"""
__version__ = "1.0.0"
__author__ = "MedEvidence Team"
__license__ = "Apache-2.0"

from .models.schemas import QueryRequest, SearchResponse
from .services.search_service import SearchService

__all__ = ["QueryRequest", "SearchResponse", "SearchService"]
