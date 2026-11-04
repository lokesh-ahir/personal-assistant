"""
Search service implementations for web search functionality.

This module provides search capabilities using various search providers.
"""

from typing import List, Optional
from pydantic import BaseModel
from src.core.config import Config
from src.services.interfaces import ISearchService


class SearchResult(BaseModel):
    """Model for search results."""
    position: int
    title: str
    url: str
    snippet: Optional[str] = None
    site_name: Optional[str] = None


class SearchResponse(BaseModel):
    """Model for search response."""
    query: str
    results: List[SearchResult]
    total_results: int


class TinyFishSearchService(ISearchService):
    """
    Search service implementation using TinyFish API.
    
    This service provides web search capabilities using the TinyFish Search API.
    Free tier: 12,000 requests per day
    """
    
    def __init__(self):
        """Initialize the TinyFish search service."""
        try:
            from tinyfish import TinyFish
            self.client = TinyFish(api_key=Config.TINYFISH_API_KEY)
        except ImportError:
            raise ImportError(
                "tinyfish package is required for TinyFishSearchService. "
                "Install it with: pip install tinyfish"
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize TinyFish client: {str(e)}")
    
    def search(self, query: str, limit: int = 10, **kwargs) -> SearchResponse:
        """
        Perform a web search using TinyFish API.
        
        Args:
            query: The search query string
            limit: Maximum number of results to return (default: 10)
            **kwargs: Additional search parameters (location, language, domain_type, etc.)
            
        Returns:
            SearchResponse containing the search results
            
        Raises:
            Exception: If the search fails
        """
        try:
            # Build search parameters
            params = {"query": query, "limit": limit}
            params.update(kwargs)
            
            # Perform the search
            response = self.client.search.query(**params)
            
            # Convert results to our format
            results = []
            for result in response.results:
                results.append(SearchResult(
                    position=result.position,
                    title=result.title,
                    url=result.url,
                    snippet=result.snippet,
                    site_name=result.site_name
                ))
            
            return SearchResponse(
                query=query,
                results=results,
                total_results=response.total_results
            )
            
        except Exception as e:
            raise Exception(f"TinyFish search failed: {str(e)}")
