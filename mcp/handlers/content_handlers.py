"""
Content Extraction Tool Handlers
"""

import mcp.types as types
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import call_api


async def handle_content_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle content extraction tool execution"""
    
    if name == "browser_get_content":
        tab_id = arguments["tab_id"]
        format_type = arguments.get("format", "markdown")
        method = arguments.get("method", "html2text")
        clean = arguments.get("clean", True)
        
        result = await call_api(
            "GET",
            f"/tab/{tab_id}/content",
            params={"format": format_type, "method": method, "clean": clean}
        )
        
        if result.get("success"):
            content = result.get("content", {})
            
            if format_type == "markdown":
                markdown = content.get("markdown", "")
                conversion = content.get("conversion", {})
                metadata = conversion.get("metadata", {})
                
                # Build info header
                info_lines = [
                    f"📄 Page: {content.get('title', 'Unknown')}",
                    f"🔗 URL: {content.get('url', 'Unknown')}",
                    f"📊 Stats: {conversion.get('length', 0)} chars, {conversion.get('lines', 0)} lines",
                    f"🔧 Method: {conversion.get('method', 'unknown')}",
                    ""
                ]
                
                if metadata:
                    info_lines.append(
                        f"📑 Elements: {metadata.get('headings', 0)} headings, "
                        f"{metadata.get('paragraphs', 0)} paragraphs, "
                        f"{metadata.get('links', 0)} links, "
                        f"{metadata.get('images', 0)} images"
                    )
                    info_lines.append("")
                
                info_lines.append("─" * 70)
                info_lines.append("")
                
                info = "\n".join(info_lines)
                
                return [types.TextContent(
                    type="text",
                    text=info + markdown
                )]
            else:
                # HTML format
                html = content.get("html", "")
                body_html = content.get("bodyHtml", "")
                
                # Return body HTML (more useful than full HTML)
                preview = body_html[:2000] if len(body_html) > 2000 else body_html
                truncated = "...\n\n[Content truncated. Use markdown format for full content]" if len(body_html) > 2000 else ""
                
                return [types.TextContent(
                    type="text",
                    text=f"HTML content from {content.get('title', 'Unknown')}\n"
                         f"URL: {content.get('url', 'Unknown')}\n"
                         f"Length: {len(html)} characters\n\n"
                         f"Body HTML:\n{preview}{truncated}"
                )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to get content: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "browser_get_metadata":
        tab_id = arguments["tab_id"]
        result = await call_api("GET", f"/tab/{tab_id}/metadata")
        
        if result.get("success"):
            metadata = result.get("metadata", {})
            
            lines = [
                f"📄 Title: {metadata.get('title', 'N/A')}",
                f"🔗 URL: {metadata.get('url', 'N/A')}",
                f"📝 Description: {metadata.get('description', 'N/A')}",
                f"🏷️  Keywords: {', '.join(metadata.get('keywords', [])) or 'N/A'}",
                f"✍️  Author: {metadata.get('author', 'N/A')}",
                ""
            ]
            
            if metadata.get('ogTitle'):
                lines.append(f"🌐 OG Title: {metadata['ogTitle']}")
            if metadata.get('ogDescription'):
                lines.append(f"🌐 OG Description: {metadata['ogDescription']}")
            
            return [types.TextContent(
                type="text",
                text="\n".join(lines)
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to get metadata: {result.get('error', 'Unknown error')}"
            )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Unknown content tool: {name}"
        )]
