"""
Test script for MCP server
Tests the MCP server functionality without Claude Desktop
"""

import asyncio
import json
from utils import call_api, get_client


async def test_mcp_server():
    """Test MCP server functionality"""
    print("=" * 70)
    print("MCP SERVER TEST")
    print("=" * 70)
    print()
    
    # Test 1: Check API health
    print("Test 1: Checking API server health...")
    try:
        result = await call_api("GET", "/health")
        if result.get("status") == "healthy":
            print(f"✓ API server is healthy")
            print(f"  Extension connected: {result.get('extension', {}).get('connected')}")
        else:
            print(f"❌ API server unhealthy: {result}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        print("   Make sure the server is running: python main.py")
        return
    print()
    
    # Test 2: List tabs
    print("Test 2: Listing browser tabs...")
    try:
        result = await call_api("GET", "/tabs")
        if result.get("success"):
            tabs = result.get("tabs", [])
            print(f"✓ Found {len(tabs)} tabs")
            for tab in tabs[:3]:  # Show first 3
                print(f"  - Tab {tab['id']}: {tab['title'][:50]}")
        else:
            print(f"❌ Failed to list tabs: {result.get('error')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 3: Create tab
    print("Test 3: Creating new tab...")
    try:
        result = await call_api(
            "POST",
            "/tab/new",
            json={"url": "https://example.com", "active": True}
        )
        if result.get("success"):
            tab = result.get("tab", {})
            tab_id = tab.get("id")
            print(f"✓ Tab created: {tab_id}")
            print(f"  URL: {tab.get('url')}")
            
            # Wait for page load
            print("  Waiting for page to load...")
            await asyncio.sleep(3)
            
            # Test 4: Extract content
            print()
            print("Test 4: Extracting content as markdown...")
            result = await call_api(
                "GET",
                f"/tab/{tab_id}/content",
                params={"format": "markdown", "method": "html2text"}
            )
            
            if result.get("success"):
                content = result.get("content", {})
                markdown = content.get("markdown", "")
                conversion = content.get("conversion", {})
                
                print(f"✓ Content extracted")
                print(f"  Method: {conversion.get('method')}")
                print(f"  Length: {conversion.get('length')} characters")
                print(f"  Lines: {conversion.get('lines')}")
                print()
                print("  First 200 characters:")
                print("  " + "-" * 66)
                print("  " + markdown[:200].replace("\n", "\n  "))
                print("  " + "-" * 66)
            else:
                print(f"❌ Failed to extract content: {result.get('error')}")
            
            # Test 5: Interact with page
            print()
            print("Test 5: Testing page interaction...")
            result = await call_api(
                "POST",
                f"/tab/{tab_id}/interact",
                json={"action": "findElement", "selector": "h1"}
            )
            
            if result.get("success"):
                res = result.get("result", {})
                if res.get("found"):
                    element = res.get("element", {})
                    print(f"✓ Element found")
                    print(f"  Tag: {element.get('tag')}")
                    print(f"  Text: {element.get('text', '')[:50]}")
                else:
                    print(f"✓ Interaction working (element not found)")
            else:
                print(f"❌ Failed to interact: {result.get('error')}")
            
            # Clean up
            print()
            print("Cleaning up...")
            await call_api("DELETE", f"/tab/{tab_id}")
            print(f"✓ Tab {tab_id} closed")
            
        else:
            print(f"❌ Failed to create tab: {result.get('error')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    print("=" * 70)
    print("MCP SERVER TEST COMPLETED")
    print("=" * 70)
    print()
    print("The MCP server is ready to use with Claude Desktop!")
    print()
    print("Next steps:")
    print("1. Add server to Claude Desktop config")
    print("2. Restart Claude Desktop")
    print("3. Try: 'List all open browser tabs'")


async def cleanup():
    """Cleanup HTTP client"""
    client = get_client()
    await client.close()


if __name__ == "__main__":
    try:
        asyncio.run(test_mcp_server())
    except KeyboardInterrupt:
        print("\nTest interrupted")
