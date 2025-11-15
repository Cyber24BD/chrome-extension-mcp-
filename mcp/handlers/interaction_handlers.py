"""
Browser Interaction Tool Handlers
"""

import mcp.types as types
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import call_api


async def handle_interaction_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle browser interaction tool execution"""
    
    tab_id = arguments["tab_id"]
    selector = arguments.get("selector")
    
    if name == "browser_click":
        result = await call_api(
            "POST",
            f"/tab/{tab_id}/interact",
            json={"action": "click", "selector": selector}
        )
        
        if result.get("success"):
            res = result.get("result", {})
            element_info = f"{res.get('elementTag', 'unknown')}"
            if res.get('elementText'):
                element_info += f" - {res.get('elementText')[:50]}"
            
            return [types.TextContent(
                type="text",
                text=f"✓ Clicked element: {selector}\n\nElement: {element_info}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to click: {result.get('error', 'Unknown error')}\n\n"
                     f"Selector: {selector}\n"
                     f"Tip: Verify the selector using browser DevTools (F12)"
            )]
    
    elif name == "browser_input":
        value = arguments["value"]
        
        result = await call_api(
            "POST",
            f"/tab/{tab_id}/interact",
            json={"action": "input", "selector": selector, "value": value}
        )
        
        if result.get("success"):
            res = result.get("result", {})
            return [types.TextContent(
                type="text",
                text=f"✓ Input filled: {selector}\n\n"
                     f"Value: {value}\n"
                     f"Element: {res.get('elementTag', 'unknown')} ({res.get('elementType', 'text')})"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to input: {result.get('error', 'Unknown error')}\n\n"
                     f"Selector: {selector}\n"
                     f"Value: {value}"
            )]
    
    elif name == "browser_get_text":
        result = await call_api(
            "POST",
            f"/tab/{tab_id}/interact",
            json={"action": "getText", "selector": selector}
        )
        
        if result.get("success"):
            text = result.get("result", {}).get("text", "")
            return [types.TextContent(
                type="text",
                text=f"Text from {selector}:\n\n{text}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to get text: {result.get('error', 'Unknown error')}\n\n"
                     f"Selector: {selector}"
            )]
    
    elif name == "browser_wait_for_element":
        timeout = arguments.get("timeout", 5000)
        
        result = await call_api(
            "POST",
            f"/tab/{tab_id}/interact",
            json={"action": "waitForElement", "selector": selector, "timeout": timeout}
        )
        
        if result.get("success"):
            return [types.TextContent(
                type="text",
                text=f"✓ Element appeared: {selector}\n\nWait time: {timeout}ms"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Element did not appear within {timeout}ms\n\n"
                     f"Selector: {selector}\n"
                     f"Error: {result.get('error', 'Timeout')}"
            )]
    
    elif name == "browser_find_element":
        result = await call_api(
            "POST",
            f"/tab/{tab_id}/interact",
            json={"action": "findElement", "selector": selector}
        )
        
        if result.get("success"):
            res = result.get("result", {})
            if res.get("found"):
                element = res.get("element", {})
                pos = element.get("position", {})
                
                info = [
                    f"✓ Element found: {selector}",
                    "",
                    f"Tag: {element.get('tag')}",
                    f"ID: {element.get('id') or 'N/A'}",
                    f"Class: {element.get('className') or 'N/A'}",
                    f"Text: {element.get('text', '')[:100]}",
                    f"Visible: {'Yes' if element.get('visible') else 'No'}",
                    f"Position: x={pos.get('x')}, y={pos.get('y')}",
                    f"Size: {pos.get('width')}x{pos.get('height')}px"
                ]
                
                return [types.TextContent(
                    type="text",
                    text="\n".join(info)
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Element not found: {selector}"
                )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to find element: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "browser_select_option":
        value = arguments["value"]
        
        result = await call_api(
            "POST",
            f"/tab/{tab_id}/interact",
            json={"action": "select", "selector": selector, "value": value}
        )
        
        if result.get("success"):
            return [types.TextContent(
                type="text",
                text=f"✓ Option selected: {selector}\n\nValue: {value}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to select option: {result.get('error', 'Unknown error')}\n\n"
                     f"Selector: {selector}\n"
                     f"Value: {value}"
            )]
    
    elif name == "browser_get_attribute":
        attribute = arguments["attribute"]
        
        result = await call_api(
            "POST",
            f"/tab/{tab_id}/interact",
            json={"action": "getAttribute", "selector": selector, "value": attribute}
        )
        
        if result.get("success"):
            res = result.get("result", {})
            attr_value = res.get("value", "")
            return [types.TextContent(
                type="text",
                text=f"Attribute '{attribute}' from {selector}:\n\n{attr_value}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to get attribute: {result.get('error', 'Unknown error')}\n\n"
                     f"Selector: {selector}\n"
                     f"Attribute: {attribute}"
            )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Unknown interaction tool: {name}"
        )]
