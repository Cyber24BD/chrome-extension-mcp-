# Advanced Markdown Conversion Guide

Complete guide for converting web pages to high-quality Markdown using Python-based conversion.

## Overview

The Browser Automation API uses **Python-based markdown conversion** instead of JavaScript libraries. This provides:

- ✓ **Better Quality**: Advanced formatting and structure preservation
- ✓ **More Control**: Multiple conversion methods and options
- ✓ **Cleaner Output**: Automatic HTML cleaning and post-processing
- ✓ **Rich Metadata**: Extract statistics about the content
- ✓ **No Browser Dependencies**: Conversion happens server-side

---

## How It Works

```
Browser → Extension → HTML → Python Server → Markdown
                      ↓
                  (Always HTML)
                      ↓
              Advanced Converter
                      ↓
              Clean Markdown
```

1. **Extension extracts HTML** from the page
2. **Python receives HTML** content
3. **Converter processes** with selected method
4. **Returns formatted Markdown** with metadata

---

## Conversion Methods

### 1. html2text (Default - Recommended)

**Best for:** Complex content, articles, documentation, Wikipedia

**Features:**
- Excellent table preservation
- Perfect code block formatting
- Maintains list structures
- Configurable line wrapping
- Inline link format
- Unicode support

**Example:**
```python
response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={
        "format": "markdown",
        "method": "html2text",
        "clean": True
    }
)
```

**Output Quality:** ⭐⭐⭐⭐⭐

---

### 2. markdownify

**Best for:** Simple pages, basic content, speed

**Features:**
- Fast conversion
- Clean, minimal output
- Good for basic HTML
- Lightweight processing

**Example:**
```python
response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={
        "format": "markdown",
        "method": "markdownify",
        "clean": True
    }
)
```

**Output Quality:** ⭐⭐⭐⭐

---

### 3. auto

**Best for:** Unknown content types, fallback scenarios

**Features:**
- Tries html2text first
- Falls back to markdownify if error
- Automatic method selection

**Example:**
```python
response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={
        "format": "markdown",
        "method": "auto",
        "clean": True
    }
)
```

---

## API Endpoint

```
GET /tab/{tab_id}/content
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | string | "html" | Output format: "html" or "markdown" |
| `method` | string | "html2text" | Conversion method: "html2text", "markdownify", "auto" |
| `clean` | boolean | true | Clean HTML before conversion |

### Response Structure

```json
{
  "success": true,
  "content": {
    "format": "markdown",
    "markdown": "# Page Title\n\nContent here...",
    "url": "https://example.com",
    "title": "Page Title",
    "timestamp": "2025-11-15T10:30:00.000Z",
    "conversion": {
      "method": "html2text",
      "length": 5432,
      "lines": 123,
      "metadata": {
        "title": "Page Title",
        "description": "Page description",
        "keywords": "keyword1, keyword2",
        "headings": 12,
        "paragraphs": 45,
        "links": 23,
        "images": 8,
        "tables": 3,
        "lists": 6
      }
    }
  }
}
```

---

## HTML Cleaning

When `clean=true` (default), the converter automatically:

### Removes:
- `<script>` tags and JavaScript
- `<style>` tags and CSS
- `<noscript>` elements
- HTML comments
- Hidden elements (`display: none`)
- Advertisement containers
- Cookie banners
- Popups and modals

### Preserves:
- Main content structure
- Headings and hierarchy
- Tables and lists
- Links and images
- Code blocks
- Semantic HTML

---

## Usage Examples

### Basic Extraction

```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

# Extract as markdown
response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={"format": "markdown"}
)

markdown = response.json()["content"]["markdown"]
print(markdown)
```

### With Metadata

```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={"format": "markdown", "method": "html2text"}
)

content = response.json()["content"]
conversion = content["conversion"]
metadata = conversion["metadata"]

print(f"Title: {content['title']}")
print(f"Length: {conversion['length']} characters")
print(f"Headings: {metadata['headings']}")
print(f"Links: {metadata['links']}")
print(f"Images: {metadata['images']}")
print(f"Tables: {metadata['tables']}")
```

### Save to File

```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={"format": "markdown", "method": "html2text"}
)

content = response.json()["content"]

# Create markdown file with frontmatter
with open("output.md", "w", encoding="utf-8") as f:
    f.write("---\n")
    f.write(f"title: {content['title']}\n")
    f.write(f"url: {content['url']}\n")
    f.write(f"date: {content['timestamp']}\n")
    f.write("---\n\n")
    f.write(content['markdown'])

print("Saved to output.md")
```

### Batch Conversion

```python
import requests
import time

BASE_URL = "http://localhost:8000"

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

for url in urls:
    # Create tab
    response = requests.post(f"{BASE_URL}/tab/new", json={"url": url})
    tab_id = response.json()["tab"]["id"]
    
    # Wait for load
    time.sleep(3)
    
    # Extract markdown
    response = requests.get(
        f"{BASE_URL}/tab/{tab_id}/content",
        params={"format": "markdown", "method": "html2text"}
    )
    
    markdown = response.json()["content"]["markdown"]
    
    # Save to file
    filename = url.split("/")[-1] + ".md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    # Close tab
    requests.delete(f"{BASE_URL}/tab/{tab_id}")
    
    print(f"Saved: {filename}")
```

### Compare Methods

```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

methods = ["html2text", "markdownify"]

for method in methods:
    response = requests.get(
        f"{BASE_URL}/tab/{tab_id}/content",
        params={"format": "markdown", "method": method}
    )
    
    content = response.json()["content"]
    conversion = content["conversion"]
    
    print(f"\nMethod: {method}")
    print(f"Length: {conversion['length']} characters")
    print(f"Lines: {conversion['lines']}")
    print(f"First 200 chars:\n{content['markdown'][:200]}")
```

---

## Best Practices

### 1. Choose the Right Method

```python
# For Wikipedia, documentation, articles
method = "html2text"

# For simple blogs, basic pages
method = "markdownify"

# For unknown content
method = "auto"
```

### 2. Always Clean HTML

```python
# Recommended (default)
params = {"format": "markdown", "clean": True}

# Only disable if you need raw conversion
params = {"format": "markdown", "clean": False}
```

### 3. Wait for Page Load

```python
# Create tab
response = requests.post(f"{BASE_URL}/tab/new", json={"url": url})
tab_id = response.json()["tab"]["id"]

# Wait for dynamic content
time.sleep(3)  # Adjust based on page complexity

# Then extract
response = requests.get(f"{BASE_URL}/tab/{tab_id}/content", ...)
```

### 4. Handle Errors

```python
try:
    response = requests.get(
        f"{BASE_URL}/tab/{tab_id}/content",
        params={"format": "markdown"}
    )
    
    result = response.json()
    
    if not result.get("success"):
        print(f"Error: {result.get('error')}")
    else:
        markdown = result["content"]["markdown"]
        # Process markdown
        
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### 5. Use Metadata

```python
response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={"format": "markdown"}
)

metadata = response.json()["content"]["conversion"]["metadata"]

# Check if content is substantial
if metadata["paragraphs"] < 5:
    print("Warning: Low content quality")

# Check for rich content
if metadata["tables"] > 0:
    print("Contains tables - html2text recommended")
```

---

## Comparison: JavaScript vs Python Conversion

### Old Approach (JavaScript - Turndown.js)

❌ **Limitations:**
- Runs in browser context
- Limited configuration options
- Inconsistent results across pages
- No HTML cleaning
- No metadata extraction
- Browser-dependent

### New Approach (Python - html2text/markdownify)

✅ **Advantages:**
- Server-side processing
- Multiple conversion methods
- Automatic HTML cleaning
- Rich metadata extraction
- Consistent results
- Highly configurable
- Better error handling

---

## Troubleshooting

### Empty Markdown Output

**Problem:** Markdown is empty or very short

**Solutions:**
1. Wait longer for page to load
2. Check if page uses dynamic content (JavaScript)
3. Try different conversion method
4. Disable cleaning: `clean=False`

### Poor Formatting

**Problem:** Markdown formatting is broken

**Solutions:**
1. Try different method (html2text vs markdownify)
2. Enable cleaning: `clean=True`
3. Check source HTML quality

### Missing Content

**Problem:** Some content is missing

**Solutions:**
1. Disable cleaning to see if content was removed
2. Check if content is in iframe
3. Wait for dynamic content to load
4. Extract specific selector instead of full page

---

## Advanced Configuration

### Custom Converter Options

For advanced use cases, you can modify the converter in `app/services/markdown_converter.py`:

```python
# Configure html2text
self.h2t.body_width = 0  # No line wrapping
self.h2t.ignore_links = False  # Include links
self.h2t.ignore_images = False  # Include images
self.h2t.inline_links = True  # Use inline link format
self.h2t.unicode_snob = True  # Use Unicode characters
```

---

## Performance

### Conversion Speed

| Method | Speed | Quality | Use Case |
|--------|-------|---------|----------|
| html2text | Medium | Excellent | Complex content |
| markdownify | Fast | Good | Simple content |
| auto | Variable | Good | Unknown content |

### Optimization Tips

1. **Reuse tabs** for multiple extractions
2. **Batch process** multiple pages
3. **Use appropriate method** for content type
4. **Enable cleaning** to reduce processing time

---

## Related Documentation

- [API Reference](API.md)
- [Content Extraction](CONTENT_EXTRACTION.md)
- [Tab Management](TAB_MANAGEMENT.md)
- [Troubleshooting](TROUBLESHOOTING.md)

---

## Examples

See `sample/test_advanced_markdown.py` for complete working examples.

Run the test:
```bash
python sample/test_advanced_markdown.py
```

Or use the batch script:
```bash
scripts\test_advanced_markdown.bat
```
