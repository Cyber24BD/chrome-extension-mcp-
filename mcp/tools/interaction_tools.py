"""
Browser Interaction Tools
"""

import mcp.types as types


def get_interaction_tools() -> list[types.Tool]:
    """Get browser interaction tool definitions"""
    return [
        types.Tool(
            name="browser_click",
            description="Click an element on the page using CSS selector (e.g., '#button-id', '.btn-class', '[name=\"submit\"]')",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of element to click. Examples: '#button-id', '.btn-primary', 'button[type=\"submit\"]'"
                    }
                },
                "required": ["tab_id", "selector"]
            }
        ),
        types.Tool(
            name="browser_input",
            description="Fill an input field with text using CSS selector",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of input field. Examples: '#username', 'input[name=\"email\"]', '.search-box'"
                    },
                    "value": {
                        "type": "string",
                        "description": "Text to input into the field"
                    }
                },
                "required": ["tab_id", "selector", "value"]
            }
        ),
        types.Tool(
            name="browser_get_text",
            description="Get text content from an element using CSS selector",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of element. Examples: 'h1', '.title', '#result'"
                    }
                },
                "required": ["tab_id", "selector"]
            }
        ),
        types.Tool(
            name="browser_wait_for_element",
            description="Wait for an element to appear on the page (useful for dynamic content)",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of element to wait for"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in milliseconds (default: 5000)",
                        "default": 5000
                    }
                },
                "required": ["tab_id", "selector"]
            }
        ),
        types.Tool(
            name="browser_find_element",
            description="Find an element and get its details (tag, id, class, text, position, visibility)",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of element to find"
                    }
                },
                "required": ["tab_id", "selector"]
            }
        ),
        types.Tool(
            name="browser_select_option",
            description="Select an option from a dropdown menu",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of select element"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value of option to select"
                    }
                },
                "required": ["tab_id", "selector", "value"]
            }
        ),
        types.Tool(
            name="browser_get_attribute",
            description="Get an attribute value from an element (e.g., href, src, data-*)",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of element"
                    },
                    "attribute": {
                        "type": "string",
                        "description": "Attribute name to get (e.g., 'href', 'src', 'data-id')"
                    }
                },
                "required": ["tab_id", "selector", "attribute"]
            }
        )
    ]
