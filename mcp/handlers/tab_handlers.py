"""
Tab Management Tool Handlers
"""

import mcp.types as types
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import call_api


async def handle_tab_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tab management tool execution"""
    
    if name == "browser_create_tab":
        result = await call_api(
            "POST",
            "/tab/new",
            json={
                "url": arguments["url"],
                "active": arguments.get("active", True)
            }
        )
        
        if result.get("success"):
            tab = result.get("tab", {})
            return [types.TextContent(
                type="text",
                text=f"✓ Tab created successfully\n\nTab ID: {tab.get('id')}\nURL: {arguments['url']}\nTitle: {tab.get('title', 'Loading...')}\n\nUse this Tab ID for further operations."
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to create tab: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "browser_list_tabs":
        result = await call_api("GET", "/tabs")
        
        if result.get("success"):
            tabs = result.get("tabs", [])
            if not tabs:
                return [types.TextContent(
                    type="text",
                    text="No tabs are currently open."
                )]
            
            tab_list = []
            for tab in tabs:
                active_marker = "🟢 " if tab.get("active") else "   "
                tab_list.append(
                    f"{active_marker}Tab {tab['id']}: {tab['title'][:60]}\n"
                    f"   URL: {tab['url']}"
                )
            
            return [types.TextContent(
                type="text",
                text=f"Found {len(tabs)} open tabs:\n\n" + "\n\n".join(tab_list)
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to list tabs: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "browser_close_tab":
        tab_id = arguments["tab_id"]
        result = await call_api("DELETE", f"/tab/{tab_id}")
        
        if result.get("success"):
            return [types.TextContent(
                type="text",
                text=f"✓ Tab {tab_id} closed successfully"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to close tab: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "browser_navigate":
        tab_id = arguments["tab_id"]
        url = arguments["url"]
        result = await call_api("POST", f"/tab/{tab_id}/navigate", params={"url": url})
        
        if result.get("success"):
            tab = result.get("tab", {})
            return [types.TextContent(
                type="text",
                text=f"✓ Navigated to {url}\n\nTab ID: {tab_id}\nTitle: {tab.get('title', 'Loading...')}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to navigate: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "browser_activate_tab":
        tab_id = arguments["tab_id"]
        result = await call_api("POST", f"/tab/{tab_id}/activate")
        
        if result.get("success"):
            return [types.TextContent(
                type="text",
                text=f"✓ Tab {tab_id} activated (brought to front)"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to activate tab: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "browser_reload_tab":
        tab_id = arguments["tab_id"]
        bypass_cache = arguments.get("bypass_cache", False)
        result = await call_api(
            "POST",
            f"/tab/{tab_id}/reload",
            params={"bypass_cache": bypass_cache}
        )
        
        if result.get("success"):
            cache_msg = " (bypassing cache)" if bypass_cache else ""
            return [types.TextContent(
                type="text",
                text=f"✓ Tab {tab_id} reloaded{cache_msg}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to reload tab: {result.get('error', 'Unknown error')}"
            )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Unknown tab tool: {name}"
        )]
