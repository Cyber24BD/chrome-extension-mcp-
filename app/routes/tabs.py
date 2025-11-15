"""Tab management routes"""

from fastapi import APIRouter, HTTPException
from app.models import (
    TabCreate, TabsResponse, TabContentResponse, 
    InteractionRequest, InteractionResponse
)
from app.services.extension import extension_service

router = APIRouter()

@router.post("/new", response_model=dict)
async def create_tab(request: TabCreate):
    """
    Open a new tab with the specified URL
    
    - **url**: The URL to open
    - **active**: Whether to make the tab active (default: true)
    """
    response = await extension_service.send_command({
        "action": "createTab",
        "url": request.url,
        "active": request.active
    })
    return response

@router.get("s", response_model=TabsResponse)
async def get_tabs(active: bool = None, current_window: bool = None):
    """
    Get information about all open tabs
    
    - **active**: Filter by active status (optional)
    - **current_window**: Filter by current window (optional)
    
    Returns a list of all tabs with their ID, URL, title, status, and more
    """
    filter_params = {}
    if active is not None:
        filter_params['active'] = active
    if current_window is not None:
        filter_params['currentWindow'] = current_window
    
    response = await extension_service.send_command({
        "action": "getTabs",
        "filter": filter_params
    })
    return response

@router.get("/active")
async def get_active_tab():
    """
    Get the currently active tab
    
    Returns information about the active tab in the current window
    """
    response = await extension_service.send_command({
        "action": "getActiveTab"
    })
    return response

@router.post("/{tab_id}/navigate")
async def navigate_tab(tab_id: int, url: str):
    """
    Navigate a tab to a new URL
    
    - **tab_id**: The ID of the tab to navigate
    - **url**: The URL to navigate to
    
    Navigates the specified tab to the new URL and waits for it to load
    """
    response = await extension_service.send_command({
        "action": "navigateTab",
        "tabId": tab_id,
        "url": url
    })
    return response

@router.post("/{tab_id}/activate")
async def activate_tab(tab_id: int):
    """
    Activate (focus) a specific tab
    
    - **tab_id**: The ID of the tab to activate
    
    Makes the specified tab active and brings it to the foreground
    """
    response = await extension_service.send_command({
        "action": "activateTab",
        "tabId": tab_id
    })
    return response

@router.post("/{tab_id}/reload")
async def reload_tab(tab_id: int, bypass_cache: bool = False):
    """
    Reload a specific tab
    
    - **tab_id**: The ID of the tab to reload
    - **bypass_cache**: Whether to bypass the cache (default: false)
    
    Reloads the specified tab and waits for it to finish loading
    """
    response = await extension_service.send_command({
        "action": "reloadTab",
        "tabId": tab_id,
        "bypassCache": bypass_cache
    })
    return response

@router.get("/{tab_id}/content")
async def get_tab_content(
    tab_id: int, 
    format: str = "html",
    method: str = "html2text",
    clean: bool = True
):
    """
    Get the content of a specific tab
    
    - **tab_id**: The ID of the tab
    - **format**: Content format - "html" or "markdown" (default: html)
    - **method**: Markdown conversion method - "html2text", "markdownify", or "auto" (default: html2text)
    - **clean**: Clean HTML before conversion (default: true)
    
    Returns the content in the requested format with metadata
    """
    try:
        # Get HTML content from extension
        response = await extension_service.send_command({
            "action": "getContent",
            "tabId": tab_id,
            "format": format
        })
        
        if not response.get("success"):
            raise HTTPException(status_code=500, detail="Failed to get content from extension")
        
        content = response.get("content", {})
        
        # If markdown is requested, convert using Python
        if format == "markdown":
            from app.services.markdown_converter import markdown_converter
            
            html = content.get("bodyHtml") or content.get("html", "")
            
            if not html:
                raise HTTPException(status_code=500, detail="No HTML content available")
            
            # Convert HTML to Markdown
            conversion_result = markdown_converter.convert(
                html=html,
                method=method,
                clean=clean
            )
            
            if not conversion_result.get("success"):
                raise HTTPException(
                    status_code=500, 
                    detail=f"Markdown conversion failed: {conversion_result.get('error')}"
                )
            
            # Return markdown content with metadata
            return {
                "success": True,
                "content": {
                    "format": "markdown",
                    "markdown": conversion_result["markdown"],
                    "html": html if format == "markdown" else None,
                    "url": content.get("url"),
                    "title": content.get("title"),
                    "timestamp": content.get("timestamp"),
                    "conversion": {
                        "method": method,
                        "length": conversion_result["length"],
                        "lines": conversion_result["lines"],
                        "metadata": conversion_result.get("metadata", {})
                    }
                }
            }
        
        # Return HTML content as-is
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get content: {str(e)}")

@router.get("/{tab_id}/metadata")
async def get_tab_metadata(tab_id: int):
    """
    Get metadata from a specific tab
    
    - **tab_id**: The ID of the tab
    
    Returns page metadata including title, description, keywords, author, and Open Graph tags
    """
    try:
        response = await extension_service.send_command({
            "action": "getMetadata",
            "tabId": tab_id
        })
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metadata: {str(e)}")

@router.post("/{tab_id}/interact", response_model=InteractionResponse)
async def interact_with_tab(tab_id: int, request: InteractionRequest):
    """
    Interact with elements in a specific tab
    
    - **tab_id**: The ID of the tab
    - **action**: Type of interaction (click, input, select, wait, waitForElement, getText, getAttribute)
    - **selector**: CSS selector for the element (required for most actions)
    - **value**: Value for input/select actions or attribute name for getAttribute
    - **timeout**: Timeout in milliseconds (default: 5000)
    
    ## Supported Actions:
    - **click**: Click an element
    - **input**: Type text into an input field
    - **select**: Select an option from a dropdown
    - **wait**: Wait for specified milliseconds
    - **waitForElement**: Wait for an element to appear
    - **getText**: Get text content of an element
    - **getAttribute**: Get an attribute value from an element
    """
    response = await extension_service.send_command({
        "action": "interact",
        "tabId": tab_id,
        "interaction": {
            "action": request.action,
            "selector": request.selector,
            "value": request.value,
            "timeout": request.timeout
        }
    })
    return response

@router.delete("/{tab_id}")
async def close_tab(tab_id: int):
    """
    Close a specific tab
    
    - **tab_id**: The ID of the tab to close
    """
    response = await extension_service.send_command({
        "action": "closeTab",
        "tabId": tab_id
    })
    return response
