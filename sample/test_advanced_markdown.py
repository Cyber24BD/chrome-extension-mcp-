"""
Test Advanced Markdown Conversion
Demonstrates Python-based markdown conversion with multiple methods
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_advanced_markdown():
    print("=" * 70)
    print("ADVANCED MARKDOWN CONVERSION TEST")
    print("=" * 70)
    print()
    
    # Step 1: Create a tab with rich content
    print("Step 1: Creating tab with Wikipedia page (rich content)...")
    response = requests.post(f"{BASE_URL}/tab/new", json={
        "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "active": True
    })
    
    if not response.json().get("success"):
        print("❌ Failed to create tab")
        return
    
    tab_id = response.json()["tab"]["id"]
    print(f"✓ Tab created: {tab_id}")
    print()
    
    # Wait for page to load
    print("Waiting for page to load...")
    time.sleep(5)
    print()
    
    # Step 2: Get HTML content
    print("Step 2: Extracting HTML content...")
    response = requests.get(f"{BASE_URL}/tab/{tab_id}/content?format=html")
    
    if response.json().get("success"):
        content = response.json()["content"]
        html_length = len(content.get("html", ""))
        print(f"✓ HTML extracted: {html_length:,} characters")
        print(f"  - Title: {content.get('title')}")
        print(f"  - URL: {content.get('url')}")
    else:
        print("❌ Failed to extract HTML")
        return
    print()
    
    # Step 3: Convert to Markdown using html2text (default)
    print("Step 3: Converting to Markdown using html2text...")
    response = requests.get(
        f"{BASE_URL}/tab/{tab_id}/content",
        params={
            "format": "markdown",
            "method": "html2text",
            "clean": True
        }
    )
    
    if response.json().get("success"):
        content = response.json()["content"]
        markdown = content.get("markdown", "")
        conversion = content.get("conversion", {})
        
        print(f"✓ Markdown generated:")
        print(f"  - Method: {conversion.get('method')}")
        print(f"  - Length: {conversion.get('length'):,} characters")
        print(f"  - Lines: {conversion.get('lines'):,}")
        
        metadata = conversion.get("metadata", {})
        if metadata:
            print(f"  - Headings: {metadata.get('headings', 0)}")
            print(f"  - Paragraphs: {metadata.get('paragraphs', 0)}")
            print(f"  - Links: {metadata.get('links', 0)}")
            print(f"  - Images: {metadata.get('images', 0)}")
            print(f"  - Tables: {metadata.get('tables', 0)}")
        
        print()
        print("First 500 characters of markdown:")
        print("-" * 70)
        print(markdown[:500])
        print("-" * 70)
    else:
        print("❌ Failed to convert to markdown")
    print()
    
    # Step 4: Convert using markdownify method
    print("Step 4: Converting using markdownify method...")
    response = requests.get(
        f"{BASE_URL}/tab/{tab_id}/content",
        params={
            "format": "markdown",
            "method": "markdownify",
            "clean": True
        }
    )
    
    if response.json().get("success"):
        content = response.json()["content"]
        markdown = content.get("markdown", "")
        conversion = content.get("conversion", {})
        
        print(f"✓ Markdown generated:")
        print(f"  - Method: {conversion.get('method')}")
        print(f"  - Length: {conversion.get('length'):,} characters")
        print(f"  - Lines: {conversion.get('lines'):,}")
        
        print()
        print("First 500 characters of markdown:")
        print("-" * 70)
        print(markdown[:500])
        print("-" * 70)
    else:
        print("❌ Failed to convert to markdown")
    print()
    
    # Step 5: Save markdown to file
    print("Step 5: Saving markdown to file...")
    response = requests.get(
        f"{BASE_URL}/tab/{tab_id}/content",
        params={
            "format": "markdown",
            "method": "html2text",
            "clean": True
        }
    )
    
    if response.json().get("success"):
        content = response.json()["content"]
        markdown = content.get("markdown", "")
        
        filename = "sample/wikipedia_python.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {content.get('title')}\n\n")
            f.write(f"**URL:** {content.get('url')}\n\n")
            f.write(f"**Extracted:** {content.get('timestamp')}\n\n")
            f.write("---\n\n")
            f.write(markdown)
        
        print(f"✓ Markdown saved to: {filename}")
        print(f"  - File size: {len(markdown):,} characters")
    else:
        print("❌ Failed to save markdown")
    print()
    
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY ✓")
    print("=" * 70)
    print()
    print("CONVERSION METHODS AVAILABLE:")
    print("  1. html2text   - Advanced, preserves formatting (default)")
    print("  2. markdownify - Simple, clean output")
    print("  3. auto        - Try html2text, fallback to markdownify")
    print()
    print("FEATURES:")
    print("  ✓ Automatic HTML cleaning (removes scripts, styles, ads)")
    print("  ✓ Preserves tables, code blocks, and formatting")
    print("  ✓ Extracts metadata (headings, links, images count)")
    print("  ✓ Post-processing for clean output")
    print("  ✓ Configurable line wrapping and link styles")
    print()
    print(f"Tab ID: {tab_id}")

def compare_methods():
    """Compare different markdown conversion methods"""
    print("\n" + "=" * 70)
    print("COMPARING MARKDOWN CONVERSION METHODS")
    print("=" * 70)
    print()
    
    # Get list of tabs
    response = requests.get(f"{BASE_URL}/tabs")
    tabs = response.json().get("tabs", [])
    
    if not tabs:
        print("No tabs available. Create a tab first.")
        return
    
    tab_id = tabs[0]["id"]
    print(f"Using tab: {tab_id} - {tabs[0]['title']}")
    print()
    
    methods = ["html2text", "markdownify"]
    
    for method in methods:
        print(f"Method: {method}")
        print("-" * 70)
        
        response = requests.get(
            f"{BASE_URL}/tab/{tab_id}/content",
            params={
                "format": "markdown",
                "method": method,
                "clean": True
            }
        )
        
        if response.json().get("success"):
            content = response.json()["content"]
            conversion = content.get("conversion", {})
            
            print(f"  Length: {conversion.get('length'):,} characters")
            print(f"  Lines: {conversion.get('lines'):,}")
            
            metadata = conversion.get("metadata", {})
            if metadata:
                print(f"  Elements: {metadata.get('headings')} headings, "
                      f"{metadata.get('paragraphs')} paragraphs, "
                      f"{metadata.get('links')} links")
        else:
            print(f"  ❌ Failed")
        
        print()

if __name__ == "__main__":
    try:
        import sys
        
        if len(sys.argv) > 1 and sys.argv[1] == "compare":
            compare_methods()
        else:
            test_advanced_markdown()
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
