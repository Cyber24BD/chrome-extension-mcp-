# Chrome Automation API

Production-ready browser automation via REST API. Control Chrome programmatically from any application.

## Features

- **Tab Management**: Open, close, and list tabs
- **Content Extraction**: Get HTML and text content from any page
- **Page Interaction**: Click, input, select, wait for elements
- **Real-time Communication**: WebSocket-based for instant responses
- **Production Ready**: Proper error handling, logging, and configuration

## Architecture

```
chrome-automation-api/
├── main.py                 # Entry point
├── app/
│   ├── api.py             # FastAPI application
│   ├── config.py          # Configuration
│   ├── models.py          # Pydantic models
│   ├── routes/            # API routes
│   │   ├── tabs.py        # Tab operations
│   │   └── websocket.py   # WebSocket endpoint
│   └── services/          # Business logic
│       └── extension.py   # Extension communication
└── extension/             # Chrome extension
    ├── manifest.json      # Extension config
    └── background.js      # Service worker
```

## Quick Start

### 1. Install Dependencies

```bash
# Windows
install.bat

# Or manually with uv
uv pip install -r requirements.txt
```

### 2. Load Extension

1. Open Chrome: `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` folder

### 3. Start Server

```bash
# Windows
start.bat

# Or manually with uv
uv run python main.py
```

Server runs on `http://localhost:8000`

## Documentation

- **[Tab Management](TAB_MANAGEMENT.md)** - List, create, navigate, activate, reload, and close tabs
- **[Content Extraction](CONTENT_EXTRACTION.md)** - Extract content in HTML/Markdown, get metadata
- **[API Reference](API.md)** - Complete API endpoint reference
- **[Architecture](ARCHITECTURE.md)** - Extension modular architecture
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions

Interactive API docs: `http://localhost:8000/docs`

### Endpoints

#### Health Check
```bash
GET /
GET /health
```

#### Tab Operations

**Create Tab**
```bash
POST /tab/new
{
  "url": "https://example.com",
  "active": true
}
```

**List Tabs**
```bash
GET /tabs
```

**Get Content**
```bash
GET /tab/{tab_id}/content
```

**Interact**
```bash
POST /tab/{tab_id}/interact
{
  "action": "click",
  "selector": "#button-id"
}
```

**Close Tab**
```bash
DELETE /tab/{tab_id}
```

### Interaction Actions

- `click` - Click an element
- `input` - Type into input field
- `select` - Select dropdown option
- `wait` - Wait for milliseconds
- `waitForElement` - Wait for element to appear
- `getText` - Extract text content
- `getAttribute` - Get element attribute

## Configuration

Create `.env` file:

```env
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=INFO
EXTENSION_RESPONSE_TIMEOUT=30
```

## Usage Examples

### Python

```python
import requests

# Open tab
response = requests.post("http://localhost:8000/tab/new", json={
    "url": "https://example.com"
})
tab_id = response.json()["tab"]["id"]

# Interact
requests.post(f"http://localhost:8000/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": "#button"
})

# Get content
content = requests.get(f"http://localhost:8000/tab/{tab_id}/content").json()

# Close
requests.delete(f"http://localhost:8000/tab/{tab_id}")
```

### cURL

```bash
# Open tab
curl -X POST http://localhost:8000/tab/new \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# List tabs
curl http://localhost:8000/tabs

# Interact
curl -X POST http://localhost:8000/tab/123/interact \
  -H "Content-Type: application/json" \
  -d '{"action": "click", "selector": "#button"}'
```

## Error Handling

All endpoints return proper HTTP status codes:

- `200` - Success
- `500` - Server error
- `503` - Extension not connected
- `504` - Extension timeout

Error response format:
```json
{
  "detail": "Error message"
}
```

## License

MIT
