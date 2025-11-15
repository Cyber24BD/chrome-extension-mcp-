# Tab Management Guide

Complete guide to managing Chrome tabs via the API.

## Overview

The Tab Management API allows you to:
- List all open tabs
- Create new tabs
- Navigate existing tabs
- Activate/focus tabs
- Reload tabs
- Close tabs

## Endpoints

### 1. List All Tabs

Get information about all open tabs in Chrome.

**Endpoint:** `GET /tabs`

**Query Parameters:**
- `active` (optional): Filter by active status (true/false)
- `current_window` (optional): Filter by current window (true/false)

**Example:**
```bash
# Get all tabs
curl http://localhost:8000/tabs

# Get only active tabs
curl http://localhost:8000/tabs?active=true

# Get tabs in current window
curl http://localhost:8000/tabs?current_window=true
```

**Python:**
```python
import requests

# Get all tabs
response = requests.get("http://localhost:8000/tabs")
tabs = response.json()

print(f"Total tabs: {tabs['count']}")
for tab in tabs['tabs']:
    print(f"[{tab['id']}] {tab['title']}")
    print(f"    URL: {tab['url']}")
    print(f"    Active: {tab['active']}")
    print(f"    Status: {tab['status']}")
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "tabs": [
    {
      "id": 123,
      "url": "https://example.com",
      "title": "Example Domain",
      "active": true,
      "windowId": 1,
      "index": 0,
      "pinned": false,
      "status": "complete",
      "favIconUrl": "https://example.com/favicon.ico"
    }
  ]
}
```

### 2. Get Active Tab

Get the currently active tab in the current window.

**Endpoint:** `GET /tab/active`

**Example:**
```bash
curl http://localhost:8000/tab/active
```

**Python:**
```python
response = requests.get("http://localhost:8000/tab/active")
active_tab = response.json()['tab']

print(f"Active tab: {active_tab['title']}")
print(f"URL: {active_tab['url']}")
```

**Response:**
```json
{
  "success": true,
  "tab": {
    "id": 123,
    "url": "https://example.com",
    "title": "Example Domain",
    "active": true,
    "windowId": 1,
    "index": 0
  }
}
```

### 3. Create New Tab

Open a new tab with a specific URL.

**Endpoint:** `POST /tab/new`

**Body:**
```json
{
  "url": "https://example.com",
  "active": true
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/tab/new \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "active": true}'
```

**Python:**
```python
response = requests.post("http://localhost:8000/tab/new", json={
    "url": "https://example.com",
    "active": True  # Make it the active tab
})

tab = response.json()['tab']
print(f"Created tab {tab['id']}: {tab['title']}")
```

### 4. Navigate Tab

Navigate an existing tab to a new URL.

**Endpoint:** `POST /tab/{tab_id}/navigate`

**Body:**
```json
{
  "url": "https://newsite.com"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/tab/123/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```

**Python:**
```python
# Navigate tab 123 to Google
response = requests.post(
    "http://localhost:8000/tab/123/navigate",
    json={"url": "https://google.com"}
)

tab = response.json()['tab']
print(f"Navigated to: {tab['url']}")
```

### 5. Activate Tab

Make a specific tab active (bring to foreground).

**Endpoint:** `POST /tab/{tab_id}/activate`

**Example:**
```bash
curl -X POST http://localhost:8000/tab/123/activate
```

**Python:**
```python
# Activate tab 123
response = requests.post("http://localhost:8000/tab/123/activate")
print("Tab activated!")
```

### 6. Reload Tab

Reload a specific tab.

**Endpoint:** `POST /tab/{tab_id}/reload`

**Query Parameters:**
- `bypass_cache` (optional): Bypass cache (default: false)

**Example:**
```bash
# Normal reload
curl -X POST http://localhost:8000/tab/123/reload

# Hard reload (bypass cache)
curl -X POST "http://localhost:8000/tab/123/reload?bypass_cache=true"
```

**Python:**
```python
# Normal reload
requests.post("http://localhost:8000/tab/123/reload")

# Hard reload
requests.post("http://localhost:8000/tab/123/reload", params={
    "bypass_cache": True
})
```

### 7. Close Tab

Close a specific tab.

**Endpoint:** `DELETE /tab/{tab_id}`

**Example:**
```bash
curl -X DELETE http://localhost:8000/tab/123
```

**Python:**
```python
response = requests.delete("http://localhost:8000/tab/123")
print("Tab closed!")
```

## Common Use Cases

### 1. List and Filter Tabs

```python
import requests

API_BASE = "http://localhost:8000"

# Get all tabs
all_tabs = requests.get(f"{API_BASE}/tabs").json()
print(f"Total tabs: {all_tabs['count']}")

# Get only active tabs
active_tabs = requests.get(f"{API_BASE}/tabs?active=true").json()
print(f"Active tabs: {active_tabs['count']}")

# Find tabs by URL pattern
for tab in all_tabs['tabs']:
    if 'github.com' in tab['url']:
        print(f"GitHub tab: {tab['title']}")
```

### 2. Switch Between Tabs

```python
# Get all tabs
tabs = requests.get(f"{API_BASE}/tabs").json()['tabs']

# Find a specific tab
target_tab = next((t for t in tabs if 'google' in t['url']), None)

if target_tab:
    # Activate it
    requests.post(f"{API_BASE}/tab/{target_tab['id']}/activate")
    print(f"Switched to: {target_tab['title']}")
```

### 3. Refresh All Tabs

```python
# Get all tabs
tabs = requests.get(f"{API_BASE}/tabs").json()['tabs']

# Reload each tab
for tab in tabs:
    print(f"Reloading: {tab['title']}")
    requests.post(f"{API_BASE}/tab/{tab['id']}/reload")
```

### 4. Close Multiple Tabs

```python
# Get all tabs
tabs = requests.get(f"{API_BASE}/tabs").json()['tabs']

# Close tabs matching criteria
for tab in tabs:
    if 'example.com' in tab['url']:
        print(f"Closing: {tab['title']}")
        requests.delete(f"{API_BASE}/tab/{tab['id']}")
```

### 5. Navigate Multiple Tabs

```python
urls = [
    "https://github.com",
    "https://stackoverflow.com",
    "https://reddit.com"
]

# Create tabs
tab_ids = []
for url in urls:
    response = requests.post(f"{API_BASE}/tab/new", json={
        "url": url,
        "active": False  # Open in background
    })
    tab_ids.append(response.json()['tab']['id'])

print(f"Opened {len(tab_ids)} tabs")
```

### 6. Tab Monitoring

```python
import time

def monitor_tabs():
    """Monitor tab changes"""
    previous_count = 0
    
    while True:
        tabs = requests.get(f"{API_BASE}/tabs").json()
        current_count = tabs['count']
        
        if current_count != previous_count:
            print(f"Tab count changed: {previous_count} → {current_count}")
            previous_count = current_count
        
        time.sleep(2)

# Run monitor
monitor_tabs()
```

### 7. Save and Restore Session

```python
import json

# Save current tabs
tabs = requests.get(f"{API_BASE}/tabs").json()['tabs']
session = [{"url": tab['url'], "title": tab['title']} for tab in tabs]

with open('session.json', 'w') as f:
    json.dump(session, f, indent=2)

print(f"Saved {len(session)} tabs")

# Restore session later
with open('session.json', 'r') as f:
    session = json.load(f)

for item in session:
    requests.post(f"{API_BASE}/tab/new", json={
        "url": item['url'],
        "active": False
    })

print(f"Restored {len(session)} tabs")
```

## Tab Properties

Each tab object contains:

| Property | Type | Description |
|----------|------|-------------|
| `id` | int | Unique tab identifier |
| `url` | string | Current URL |
| `title` | string | Page title |
| `active` | boolean | Whether tab is active |
| `windowId` | int | Window containing the tab |
| `index` | int | Position in tab strip |
| `pinned` | boolean | Whether tab is pinned |
| `status` | string | "loading" or "complete" |
| `favIconUrl` | string | Favicon URL |

## Error Handling

```python
try:
    response = requests.post(f"{API_BASE}/tab/999/navigate", json={
        "url": "https://example.com"
    })
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e}")
    # Handle error (tab not found, etc.)
```

## Best Practices

1. **Check tab exists before operations:**
   ```python
   tabs = requests.get(f"{API_BASE}/tabs").json()['tabs']
   tab_ids = [t['id'] for t in tabs]
   
   if target_id in tab_ids:
       # Perform operation
   ```

2. **Wait for tab to load:**
   - The API automatically waits for tabs to load
   - No need for manual delays

3. **Handle closed tabs:**
   - Tab IDs become invalid after closing
   - Always get fresh tab list

4. **Batch operations:**
   - Process multiple tabs efficiently
   - Use background tabs for bulk operations

5. **Monitor status:**
   - Check `status` property
   - "loading" = still loading
   - "complete" = ready for interaction

## Complete Example

```python
import requests
import time

API_BASE = "http://localhost:8000"

def manage_tabs():
    """Complete tab management example"""
    
    # 1. List current tabs
    print("Current tabs:")
    tabs = requests.get(f"{API_BASE}/tabs").json()
    for tab in tabs['tabs']:
        print(f"  [{tab['id']}] {tab['title']}")
    
    # 2. Open new tabs
    print("\nOpening new tabs...")
    urls = ["https://github.com", "https://stackoverflow.com"]
    new_tabs = []
    
    for url in urls:
        response = requests.post(f"{API_BASE}/tab/new", json={
            "url": url,
            "active": False
        })
        new_tabs.append(response.json()['tab'])
        print(f"  Opened: {url}")
    
    # 3. Wait a bit
    time.sleep(2)
    
    # 4. Activate first new tab
    print(f"\nActivating tab: {new_tabs[0]['title']}")
    requests.post(f"{API_BASE}/tab/{new_tabs[0]['id']}/activate")
    
    # 5. Navigate second tab
    print(f"\nNavigating tab to Google...")
    requests.post(f"{API_BASE}/tab/{new_tabs[1]['id']}/navigate", json={
        "url": "https://google.com"
    })
    
    # 6. Reload first tab
    print(f"\nReloading tab...")
    requests.post(f"{API_BASE}/tab/{new_tabs[0]['id']}/reload")
    
    # 7. Close tabs
    print(f"\nClosing tabs...")
    for tab in new_tabs:
        requests.delete(f"{API_BASE}/tab/{tab['id']}")
        print(f"  Closed: {tab['title']}")
    
    print("\nDone!")

if __name__ == "__main__":
    manage_tabs()
```

## See Also

- [API Reference](API.md)
- [Content Extraction](CONTENT_EXTRACTION.md)
- [Page Interactions](INTERACTIONS.md)
