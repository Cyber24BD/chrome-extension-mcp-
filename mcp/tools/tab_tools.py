"""
Tab Management Tools
"""

import mcp.types as types


def get_tab_tools() -> list[types.Tool]:
    """Get tab management tool definitions"""
    return [
        types.Tool(
            name="browser_create_tab",
            description="Create a new browser tab and navigate to a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to open in the new tab"
                    },
                    "active": {
                        "type": "boolean",
                        "description": "Whether to make the tab active (default: true)",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="browser_list_tabs",
            description="Get a list of all open browser tabs with their IDs, titles, and URLs",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="browser_close_tab",
            description="Close a specific browser tab by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab to close"
                    }
                },
                "required": ["tab_id"]
            }
        ),
        types.Tool(
            name="browser_navigate",
            description="Navigate an existing tab to a new URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab to navigate"
                    },
                    "url": {
                        "type": "string",
                        "description": "URL to navigate to"
                    }
                },
                "required": ["tab_id", "url"]
            }
        ),
        types.Tool(
            name="browser_activate_tab",
            description="Activate (focus) a specific tab",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab to activate"
                    }
                },
                "required": ["tab_id"]
            }
        ),
        types.Tool(
            name="browser_reload_tab",
            description="Reload a tab's content",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab to reload"
                    },
                    "bypass_cache": {
                        "type": "boolean",
                        "description": "Whether to bypass cache (default: false)",
                        "default": False
                    }
                },
                "required": ["tab_id"]
            }
        )
    ]
