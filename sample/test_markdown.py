"""
Test Markdown Conversion Feature
Opens a page and gets content in both HTML and Markdown formats
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_markdown_conversion():
    """Test markdown conversion feature"""
    
    print("="*70)
    print("Markdown Conversion Test")
    print("="*70)
    
    # Check connection
    response = requests.get(API_BASE)
    if not response.json().get("extension_connected"):
        print("\n✗ Extension not connected!")
        return
    
    print("\n✓ Extension connected\n")
    
    # Open a test page
    print("1. Opening test page...")
    response = requests.post(f"{API_BASE}/tab/new", json={
        "url": "https://example.com",
        "active": True
    })
    
    tab_id = response.json()["tab"]["id"]
    print(f"   ✓ Tab opened (ID: {tab_id})\n")
    
    # Get HTML content
    print("2. Getting HTML content...")
    response = requests.get(f"{API_BASE}/tab/{tab_id}/content?format=html")
    html_content = response.json()["content"]
    print(f"   ✓ HTML received")
    print(f"   - Title: {html_content.get('title')}")
    print(f"   - URL: {html_content.get('url')}")
    print(f"   - Format: {html_content.get('format')}")
    print(f"   - HTML length: {len(html_content.get('html', ''))} bytes\n")
    
    # Get Markdown content
    print("3. Getting Markdown content...")
    response = requests.get(f"{API_BASE}/tab/{tab_id}/content?format=markdown")
    markdown_content = response.json()["content"]
    print(f"   ✓ Markdown received")
    print(f"   - Title: {markdown_content.get('title')}")
    print(f"   - Format: {markdown_content.get('format')}")
    print(f"   - Markdown length: {len(markdown_content.get('markdown', ''))} chars\n")
    
    # Get metadata
    print("4. Getting page metadata...")
    response = requests.get(f"{API_BASE}/tab/{tab_id}/metadata")
    metadata = response.json()["metadata"]
    print(f"   ✓ Metadata received")
    print(f"   - Title: {metadata.get('title')}")
    print(f"   - Description: {metadata.get('description')}")
    print(f"   - Author: {metadata.get('author')}")
    print(f"   - Keywords: {metadata.get('keywords')}\n")
    
    # Create markdown file with metadata
    print("5. Creating markdown file...")
    markdown_output = f"""---
title: {metadata.get('title')}
url: {metadata.get('url')}
description: {metadata.get('description')}
author: {metadata.get('author')}
timestamp: {metadata.get('timestamp')}
---

# {metadata.get('title')}

**URL:** {metadata.get('url')}

---

{markdown_content.get('markdown', '')}
"""
    
    # Save to file
    filename = "sample/page_content.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_output)
    
    print(f"   ✓ Markdown saved to: {filename}\n")
    
    # Save JSON results
    results = {
        "html": html_content,
        "markdown": markdown_content,
        "metadata": metadata
    }
    
    with open("sample/content_test_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("   ✓ Full results saved to: sample/content_test_results.json\n")
    
    # Close tab
    print("6. Closing tab...")
    requests.delete(f"{API_BASE}/tab/{tab_id}")
    print("   ✓ Tab closed\n")
    
    print("="*70)
    print("Test Complete!")
    print("="*70)
    print("\nMarkdown Preview:")
    print("-"*70)
    print(markdown_output[:500] + "...")

if __name__ == "__main__":
    test_markdown_conversion()
