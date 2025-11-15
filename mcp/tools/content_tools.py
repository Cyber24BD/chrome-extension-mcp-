"""
Content Extraction Tools
"""

import mcp.types as types


def get_content_tools() -> list[types.Tool]:
    """Get content extraction tool definitions"""
    return [
        types.Tool(
            name="browser_get_content",
            description="Extract content from a tab in HTML or Markdown format. Use markdown for readable text extraction.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab to extract content from"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["html", "markdown"],
                        "description": "Output format: 'html' for raw HTML, 'markdown' for readable text (default: markdown)",
                        "default": "markdown"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["html2text", "markdownify", "auto"],
                        "description": "Markdown conversion method: 'html2text' (best quality), 'markdownify' (simple), 'auto' (fallback) (default: html2text)",
                        "default": "html2text"
                    },
                    "clean": {
                        "type": "boolean",
                        "description": "Clean HTML before conversion (removes ads, scripts, styles) (default: true)",
                        "default": True
                    }
                },
                "required": ["tab_id"]
            }
        ),
        types.Tool(
            name="browser_get_metadata",
            description="Extract metadata from a page (title, description, keywords, Open Graph tags)",
            inputSchema={
                "type": "object",
                "properties": {
                    "tab_id": {
                        "type": "integer",
                        "description": "ID of the tab"
                    }
                },
                "required": ["tab_id"]
            }
        )
    ]
