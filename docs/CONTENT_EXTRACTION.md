# Content Extraction Guide

Complete guide to extracting content from web pages in HTML and Markdown formats.

## Overview

The Content Extraction API allows you to:
- Get page content in HTML format
- Convert page content to Markdown
- Extract page metadata (title, description, keywords, Open Graph tags)
- Create markdown files with frontmatter

## Endpoints

### 1. Get Page Content

Extract content from a tab in HTML or Markdown format.

**Endpoint:** `GET /tab/{tab_id}/content`

**Query Parameters:**
- `format`: Content format - "html" or "markdown" (default: "html")

**HTML Format Example:**
```bash
curl "http://localhost:8000/tab/123/content?format=html"
```

**Python:**
```python
import requests

# Get HTML content
response = requests.get("http://localhost:8000/tab/123/content", params={
    "format": "html"
})

content = response.json()['content']
print(f"Title: {content['title']}")
print(f"URL: {content['url']}")
print(f"HTML length: {len(content['html'])} bytes")
print(f"Text length: {len(content['text'])} chars")
```

**HTML Response:**
```json
{
  "success": true,
  "content": {
    "url": "https://example.com",
    "title": "Example Domain",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "html": "<!DOCTYPE html>...",
    "text": "Example Domain\nThis domain is for use...",
    "format": "html"
  }
}
```

**Markdown Format Example:**
```bash
curl "http://localhost:8000/tab/123/content?format=markdown"
```

**Python:**
```python
# Get Markdown content
response = requests.get("http://localhost:8000/tab/123/content", params={
    "format": "markdown"
})

content = response.json()['content']
print(f"Title: {content['title']}")
print(f"Markdown:\n{content['markdown']}")
```

**Markdown Response:**
```json
{
  "success": true,
  "content": {
    "url": "https://example.com",
    "title": "Example Domain",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "markdown": "# Example Domain\n\nThis domain is for use...",
    "format": "markdown"
  }
}
```

### 2. Get Page Metadata

Extract metadata from a page.

**Endpoint:** `GET /tab/{tab_id}/metadata`

**Example:**
```bash
curl http://localhost:8000/tab/123/metadata
```

**Python:**
```python
response = requests.get("http://localhost:8000/tab/123/metadata")
metadata = response.json()['metadata']

print(f"Title: {metadata['title']}")
print(f"Description: {metadata['description']}")
print(f"Keywords: {metadata['keywords']}")
print(f"Author: {metadata['author']}")
```

**Response:**
```json
{
  "success": true,
  "metadata": {
    "url": "https://example.com",
    "title": "Example Domain",
    "description": "Example Domain for documentation",
    "keywords": ["example", "domain", "documentation"],
    "author": "IANA",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "ogTitle": "Example Domain",
    "ogDescription": "This domain is for use in examples"
  }
}
```

## Markdown Conversion

The extension uses [Turndown.js](https://github.com/mixmark-io/turndown) to convert HTML to Markdown.

**Features:**
- Preserves headings (H1-H6)
- Converts links and images
- Maintains lists (ordered and unordered)
- Preserves code blocks
- Handles tables
- Cleans up unnecessary HTML

**Conversion Process:**
1. Extension receives markdown request
2. Dynamically loads Turndown.js from CDN (if not already loaded)
3. Converts page HTML to Markdown
4. Returns clean Markdown text

**Fallback:**
If Turndown.js fails to load, the extension falls back to plain text extraction.

## Use Cases

### 1. Save Page as Markdown

```python
import requests

API_BASE = "http://localhost:8000"

def save_page_as_markdown(tab_id, filename):
    """Save page content as markdown file"""
    
    # Get metadata
    metadata = requests.get(f"{API_BASE}/tab/{tab_id}/metadata").json()['metadata']
    
    # Get markdown content
    content = requests.get(
        f"{API_BASE}/tab/{tab_id}/content",
        params={"format": "markdown"}
    ).json()['content']
    
    # Create markdown with frontmatter
    markdown = f"""---
title: {metadata['title']}
url: {metadata['url']}
description: {metadata.get('description', '')}
author: {metadata.get('author', '')}
keywords: {', '.join(metadata.get('keywords', []))}
timestamp: {metadata['timestamp']}
---

# {metadata['title']}

**URL:** {metadata['url']}

---

{content['markdown']}
"""
    
    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"✓ Saved to: {filename}")

# Usage
save_page_as_markdown(123, "page.md")
```

### 2. Extract Article Content

```python
def extract_article(url):
    """Open URL and extract article content"""
    
    # Open page
    response = requests.post(f"{API_BASE}/tab/new", json={
        "url": url,
        "active": False
    })
    tab_id = response.json()['tab']['id']
    
    # Get markdown content
    content = requests.get(
        f"{API_BASE}/tab/{tab_id}/content",
        params={"format": "markdown"}
    ).json()['content']
    
    # Close tab
    requests.delete(f"{API_BASE}/tab/{tab_id}")
    
    return content['markdown']

# Usage
article = extract_article("https://example.com/article")
print(article)
```

### 3. Batch Download Pages

```python
def download_pages(urls, output_dir="downloads"):
    """Download multiple pages as markdown"""
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    for i, url in enumerate(urls):
        print(f"Downloading {i+1}/{len(urls)}: {url}")
        
        # Open page
        response = requests.post(f"{API_BASE}/tab/new", json={
            "url": url,
            "active": False
        })
        tab_id = response.json()['tab']['id']
        
        # Get content
        metadata = requests.get(f"{API_BASE}/tab/{tab_id}/metadata").json()['metadata']
        content = requests.get(
            f"{API_BASE}/tab/{tab_id}/content",
            params={"format": "markdown"}
        ).json()['content']
        
        # Save
        filename = f"{output_dir}/{i+1}_{metadata['title'][:50]}.md"
        filename = filename.replace('/', '_').replace('\\', '_')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content['markdown'])
        
        # Close tab
        requests.delete(f"{API_BASE}/tab/{tab_id}")
        
        print(f"  ✓ Saved: {filename}")

# Usage
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]
download_pages(urls)
```

### 4. Compare HTML vs Markdown

```python
def compare_formats(tab_id):
    """Compare HTML and Markdown output"""
    
    # Get HTML
    html_content = requests.get(
        f"{API_BASE}/tab/{tab_id}/content",
        params={"format": "html"}
    ).json()['content']
    
    # Get Markdown
    md_content = requests.get(
        f"{API_BASE}/tab/{tab_id}/content",
        params={"format": "markdown"}
    ).json()['content']
    
    print(f"HTML size: {len(html_content['html'])} bytes")
    print(f"Text size: {len(html_content['text'])} chars")
    print(f"Markdown size: {len(md_content['markdown'])} chars")
    print(f"\nMarkdown preview:\n{md_content['markdown'][:500]}...")

compare_formats(123)
```

### 5. Extract Metadata Only

```python
def get_page_info(url):
    """Get page metadata without full content"""
    
    # Open page
    response = requests.post(f"{API_BASE}/tab/new", json={
        "url": url,
        "active": False
    })
    tab_id = response.json()['tab']['id']
    
    # Get metadata
    metadata = requests.get(f"{API_BASE}/tab/{tab_id}/metadata").json()['metadata']
    
    # Close tab
    requests.delete(f"{API_BASE}/tab/{tab_id}")
    
    return {
        "title": metadata['title'],
        "description": metadata.get('description', ''),
        "url": metadata['url']
    }

# Usage
info = get_page_info("https://example.com")
print(f"Title: {info['title']}")
print(f"Description: {info['description']}")
```

### 6. Create Documentation

```python
def create_docs_from_urls(urls, output_file="docs.md"):
    """Create single documentation file from multiple URLs"""
    
    docs = []
    
    for url in urls:
        print(f"Processing: {url}")
        
        # Open page
        response = requests.post(f"{API_BASE}/tab/new", json={
            "url": url,
            "active": False
        })
        tab_id = response.json()['tab']['id']
        
        # Get content
        metadata = requests.get(f"{API_BASE}/tab/{tab_id}/metadata").json()['metadata']
        content = requests.get(
            f"{API_BASE}/tab/{tab_id}/content",
            params={"format": "markdown"}
        ).json()['content']
        
        # Add to docs
        docs.append(f"""
## {metadata['title']}

**Source:** {metadata['url']}

{content['markdown']}

---
""")
        
        # Close tab
        requests.delete(f"{API_BASE}/tab/{tab_id}")
    
    # Save combined docs
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Documentation\n\n")
        f.write("\n".join(docs))
    
    print(f"\n✓ Created: {output_file}")

# Usage
urls = [
    "https://example.com/guide1",
    "https://example.com/guide2"
]
create_docs_from_urls(urls)
```

## Content Properties

### HTML Format Response

| Property | Type | Description |
|----------|------|-------------|
| `url` | string | Page URL |
| `title` | string | Page title |
| `timestamp` | string | Extraction timestamp (ISO 8601) |
| `html` | string | Full HTML source |
| `text` | string | Plain text content |
| `format` | string | "html" |

### Markdown Format Response

| Property | Type | Description |
|----------|------|-------------|
| `url` | string | Page URL |
| `title` | string | Page title |
| `timestamp` | string | Extraction timestamp (ISO 8601) |
| `markdown` | string | Markdown content |
| `format` | string | "markdown" |

### Metadata Response

| Property | Type | Description |
|----------|------|-------------|
| `url` | string | Page URL |
| `title` | string | Page title |
| `description` | string | Meta description |
| `keywords` | array | Meta keywords |
| `author` | string | Meta author |
| `timestamp` | string | Extraction timestamp |
| `ogTitle` | string | Open Graph title |
| `ogDescription` | string | Open Graph description |

## Best Practices

1. **Choose the right format:**
   - Use HTML for full page source
   - Use Markdown for readable content
   - Use metadata for page info only

2. **Handle large pages:**
   - Markdown conversion may take time on large pages
   - Consider timeout settings

3. **Save with frontmatter:**
   - Include metadata in markdown files
   - Makes content searchable and organized

4. **Batch operations:**
   - Open tabs in background
   - Process multiple pages efficiently
   - Close tabs after extraction

5. **Error handling:**
   ```python
   try:
       content = requests.get(f"{API_BASE}/tab/{tab_id}/content").json()
       if not content.get('success'):
           print(f"Error: {content.get('error')}")
   except Exception as e:
       print(f"Failed: {e}")
   ```

## Complete Example

```python
import requests
import json
import time

API_BASE = "http://localhost:8000"

def extract_and_save(url, output_file):
    """Complete example: extract page and save as markdown"""
    
    print(f"Processing: {url}")
    
    # 1. Open page
    print("  Opening page...")
    response = requests.post(f"{API_BASE}/tab/new", json={
        "url": url,
        "active": False
    })
    tab_id = response.json()['tab']['id']
    
    # 2. Wait for page to load
    time.sleep(2)
    
    # 3. Get metadata
    print("  Extracting metadata...")
    metadata = requests.get(f"{API_BASE}/tab/{tab_id}/metadata").json()['metadata']
    
    # 4. Get markdown content
    print("  Converting to markdown...")
    content = requests.get(
        f"{API_BASE}/tab/{tab_id}/content",
        params={"format": "markdown"}
    ).json()['content']
    
    # 5. Create markdown file
    print("  Creating file...")
    markdown = f"""---
title: {metadata['title']}
url: {metadata['url']}
description: {metadata.get('description', '')}
author: {metadata.get('author', '')}
keywords: {', '.join(metadata.get('keywords', []))}
date: {metadata['timestamp']}
---

# {metadata['title']}

**Source:** [{metadata['url']}]({metadata['url']})

---

{content['markdown']}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    # 6. Close tab
    print("  Closing tab...")
    requests.delete(f"{API_BASE}/tab/{tab_id}")
    
    print(f"✓ Saved to: {output_file}\n")
    
    return {
        "url": url,
        "title": metadata['title'],
        "file": output_file,
        "size": len(markdown)
    }

if __name__ == "__main__":
    result = extract_and_save(
        "https://example.com",
        "example.md"
    )
    print(json.dumps(result, indent=2))
```

## See Also

- [Tab Management](TAB_MANAGEMENT.md)
- [Page Interactions](INTERACTIONS.md)
- [API Reference](API.md)
