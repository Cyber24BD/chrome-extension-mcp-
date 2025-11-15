"""Pydantic models for request/response validation"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TabCreate(BaseModel):
    """Request model for creating a new tab"""
    url: str = Field(..., description="URL to open in the new tab")
    active: bool = Field(True, description="Whether to make the tab active")

class TabInfo(BaseModel):
    """Tab information model"""
    id: int
    url: str
    title: str
    active: bool
    windowId: Optional[int] = None

class TabsResponse(BaseModel):
    """Response model for listing tabs"""
    success: bool
    tabs: List[TabInfo]

class TabContentResponse(BaseModel):
    """Response model for tab content"""
    success: bool
    content: Dict[str, Any]

class InteractionRequest(BaseModel):
    """Request model for page interactions"""
    action: str = Field(..., description="Action type: click, input, select, wait, waitForElement, getText, getAttribute")
    selector: Optional[str] = Field(None, description="CSS selector for the element")
    value: Optional[str] = Field(None, description="Value for input/select/getAttribute actions")
    timeout: int = Field(5000, description="Timeout in milliseconds")

class InteractionResponse(BaseModel):
    """Response model for interactions"""
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
