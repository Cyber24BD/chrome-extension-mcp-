"""
Extract You.com content as Markdown
Advanced test: Get specific tab content and convert to markdown
"""

import requests
import json

API_BASE = "http://localhost:8000"

def extract_youcom_content():
    """Extract content from You.com tab"""
    
    print("="*70)
    print("You.com Content Extraction Test")
    print("="*70)
    
    # Check connection
    response = requests.get(API_BASE)
    if not response.json().get("extension_connected"):
        print("\n✗ Extension not connected!")
        return
    
    print("\n✓ Extension connected\n")
    
    # 1. Get all tabs
    print("1. Finding You.com tab...")
    response = requests.get(f"{API_BASE}/tabs")
    tabs = response.json()['tabs']
    
    # Find You.com tab
    youcom_tab = None
    for tab in tabs:
        if 'you.com' in tab['url'].lower():
            youcom_tab = tab
            break
    
    if not youcom_tab:
        print("   ✗ You.com tab not found!")
        print("   Available tabs:")
        for tab in tabs:
            print(f"     - {tab['title']}: {tab['url']}")
        return
    
    print(f"   ✓ Found You.com tab: {youcom_tab['title']}")
    print(f"     Tab ID: {youcom_tab['id']}")
    print(f"     URL: {youcom_tab['url']}\n")
    
    # 2. Get metadata
    print("2. Extracting metadata...")
    try:
        response = requests.get(f"{API_BASE}/tab/{youcom_tab['id']}/metadata")
        
        if response.ok:
            result = response.json()
            metadata = result.get('metadata', {}) if result else {}
            if metadata:
                print(f"   ✓ Metadata extracted:")
                print(f"     Title: {metadata.get('title', 'N/A')}")
                desc = metadata.get('description', 'N/A')
                if desc and len(desc) > 100:
                    desc = desc[:100] + "..."
                print(f"     Description: {desc}")
                print(f"     Keywords: {metadata.get('keywords', [])}")
                print(f"     Author: {metadata.get('author', 'N/A')}\n")
            else:
                raise Exception("No metadata in response")
        else:
            raise Exception(f"HTTP {response.status_code}")
    except Exception as e:
        print(f"   ⚠ Could not get metadata: {e}")
        print("   Using basic metadata from tab info\n")
        metadata = {
            'title': youcom_tab['title'],
            'url': youcom_tab['url'],
            'description': '',
            'keywords': [],
            'author': '',
            'timestamp': ''
        }
    
    # 3. Get HTML content
    print("3. Getting HTML content...")
    response = requests.get(
        f"{API_BASE}/tab/{youcom_tab['id']}/content",
        params={"format": "html"}
    )
    
    if response.ok:
        html_content = response.json()['content']
        print(f"   ✓ HTML extracted:")
        print(f"     HTML size: {len(html_content.get('html', ''))} bytes")
        print(f"     Text size: {len(html_content.get('text', ''))} chars\n")
    else:
        print(f"   ✗ Failed to get HTML: {response.text}\n")
        return
    
    # 4. Get Markdown content
    print("4. Converting to Markdown...")
    response = requests.get(
        f"{API_BASE}/tab/{youcom_tab['id']}/content",
        params={"format": "markdown"}
    )
    
    if not response.ok:
        print(f"   ✗ Failed to get Markdown: {response.text}\n")
        return
    
    markdown_content = response.json()['content']
    markdown_text = markdown_content.get('markdown', '')
    
    print(f"   ✓ Markdown converted:")
    print(f"     Format: {markdown_content.get('format', 'N/A')}")
    print(f"     Markdown size: {len(markdown_text)} chars\n")
    
    # 5. Create markdown file with frontmatter
    print("5. Creating markdown file...")
    
    # Create frontmatter
    frontmatter = f"""---
title: {metadata.get('title', 'Untitled')}
url: {metadata.get('url', youcom_tab['url'])}
description: {metadata.get('description', '')}
author: {metadata.get('author', '')}
keywords: {', '.join(metadata.get('keywords', []))}
timestamp: {metadata.get('timestamp', markdown_content.get('timestamp', ''))}
tab_id: {youcom_tab['id']}
---

"""
    
    # Create full markdown document
    full_markdown = frontmatter + f"""# {metadata.get('title', 'Untitled')}

**Source:** [{metadata.get('url', youcom_tab['url'])}]({metadata.get('url', youcom_tab['url'])})

---

{markdown_text}
"""
    
    # Save to file
    filename = "sample/youcom_content.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(full_markdown)
    
    print(f"   ✓ Saved to: {filename}")
    print(f"   ✓ File size: {len(full_markdown)} chars\n")
    
    # 6. Save JSON results
    print("6. Saving JSON results...")
    results = {
        "tab": {
            "id": youcom_tab['id'],
            "title": youcom_tab['title'],
            "url": youcom_tab['url']
        },
        "metadata": metadata,
        "content": {
            "html_size": len(html_content.get('html', '')),
            "text_size": len(html_content.get('text', '')),
            "markdown_size": len(markdown_text),
            "format": markdown_content.get('format', 'N/A')
        }
    }
    
    with open("sample/youcom_extraction_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ Saved to: sample/youcom_extraction_results.json\n")
    
    # 7. Show preview
    print("="*70)
    print("Markdown Preview (first 500 chars)")
    print("="*70)
    print(full_markdown[:500])
    print("...")
    print("\n" + "="*70)
    print("Extraction Complete!")
    print("="*70)
    print(f"\n✓ Markdown file: {filename}")
    print(f"✓ JSON results: sample/youcom_extraction_results.json")
    print(f"✓ Total size: {len(full_markdown)} characters")

if __name__ == "__main__":
    extract_youcom_content()
