"""Tool definitions and handlers"""

from .tab_tools import get_tab_tools
from .content_tools import get_content_tools
from .interaction_tools import get_interaction_tools

__all__ = ["get_tab_tools", "get_content_tools", "get_interaction_tools"]


def get_all_tools():
    """Get all available tools"""
    return [
        *get_tab_tools(),
        *get_content_tools(),
        *get_interaction_tools()
    ]
