"""
Pydantic schemas for API request and response models.

These schemas define the data structures for API communication,
enabling validation and documentation via OpenAPI.
"""

from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    session_id: Optional[str] = "default_session"


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    session_id: str
