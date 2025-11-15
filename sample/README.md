# Sample Automation Scripts

Example scripts demonstrating Chrome Automation API usage.

## Google Search Example

Automates Google search and extracts results.

### Run

```bash
uv run python sample/google_search.py
```

### What it does

1. Opens Google.com in a new tab
2. Enters search query "cyber24bd"
3. Submits the search
4. Waits for results to load
5. Extracts page content
6. Saves results to `sample/search_results.json`
7. Closes the tab

### Output

Results are saved in JSON format:
```json
{
  "query": "cyber24bd",
  "url": "https://www.google.com/search?q=cyber24bd",
  "title": "cyber24bd - Google Search",
  "text_content": "...",
  "html_length": 123456,
  "tab_id": 123
}
```

## Customize

Modify the script to:
- Search different queries
- Extract specific elements
- Keep tab open for inspection
- Process multiple searches
- Parse search result links

### Example: Keep tab open

```python
# Comment out the close tab section
# requests.delete(f"{API_BASE}/tab/{tab_id}")
```

### Example: Extract result links

```python
# After getting content, extract links
response = requests.post(
    f"{API_BASE}/tab/{tab_id}/interact",
    json={
        "action": "getText",
        "selector": "#search a"
    }
)
```
