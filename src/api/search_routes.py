"""
API routes for search functionality.

This module provides endpoints for web search using the configured search service.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from src.services.interfaces import ISearchService
from src.core.container import container

router = APIRouter(prefix="/search", tags=["search"])


class SearchRequest(BaseModel):
    """Request model for search endpoint."""
    query: str
    limit: Optional[int] = 10
    location: Optional[str] = None
    language: Optional[str] = None
    domain_type: Optional[str] = None


class SearchResultResponse(BaseModel):
    """Response model for a single search result."""
    position: int
    title: str
    url: str
    snippet: Optional[str] = None
    site_name: Optional[str] = None


class SearchResponse(BaseModel):
    """Response model for search endpoint."""
    query: str
    results: list[SearchResultResponse]
    total_results: int


def get_search_service() -> ISearchService:
    """
    Dependency injection for search service.
    
    Returns:
        An instance of ISearchService from the container
    """
    return container.get(ISearchService)


@router.post("/", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    search_service: ISearchService = Depends(get_search_service)
):
    """
    Perform a web search using the configured search service.
    
    This endpoint accepts a search query and optional parameters,
    and returns structured search results.
    
    Args:
        request: SearchRequest containing query and optional parameters
        search_service: Injected search service instance
        
    Returns:
        SearchResponse with search results
        
    Raises:
        HTTPException: If search fails
    """
    try:
        if not request.query:
            raise HTTPException(status_code=400, detail="Query is required")

        # Build kwargs for search
        kwargs = {}
        if request.location:
            kwargs["location"] = request.location
        if request.language:
            kwargs["language"] = request.language
        if request.domain_type:
            kwargs["domain_type"] = request.domain_type

        # Perform search
        response = search_service.search(
            query=request.query,
            limit=request.limit,
            **kwargs
        )
        
        # Convert to response format
        results = []
        for result in response.results:
            results.append(SearchResultResponse(
                position=result.position,
                title=result.title,
                url=result.url,
                snippet=result.snippet,
                site_name=result.site_name
            ))
        
        return SearchResponse(
            query=response.query,
            results=results,
            total_results=response.total_results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
