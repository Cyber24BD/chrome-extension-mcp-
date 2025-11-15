"""Tool execution handlers"""

from .tab_handlers import handle_tab_tool
from .content_handlers import handle_content_tool
from .interaction_handlers import handle_interaction_tool

__all__ = ["handle_tab_tool", "handle_content_tool", "handle_interaction_tool"]


async def handle_tool(name: str, arguments: dict):
    """Route tool execution to appropriate handler"""
    
    # Tab management tools
    if name.startswith("browser_") and any(x in name for x in ["tab", "navigate", "activate", "reload"]):
        return await handle_tab_tool(name, arguments)
    
    # Content extraction tools
    elif name in ["browser_get_content", "browser_get_metadata"]:
        return await handle_content_tool(name, arguments)
    
    # Interaction tools
    elif name in ["browser_click", "browser_input", "browser_get_text", 
                  "browser_wait_for_element", "browser_find_element",
                  "browser_select_option", "browser_get_attribute"]:
        return await handle_interaction_tool(name, arguments)
    
    else:
        raise ValueError(f"Unknown tool: {name}")
