# API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required for local development.

## Endpoints

### Health Check

#### GET /

Check if server is running and extension is connected.

**Response**
```json
{
  "name": "Chrome Automation API",
  "version": "1.0.0",
  "status": "running",
  "extension_connected": true
}
```

#### GET /health

Detailed health information.

**Response**
```json
{
  "status": "healthy",
  "extension": {
    "connected": true,
    "pending_requests": 0
  }
}
```

---

### Tab Management

#### POST /tab/new

Open a new tab.

**Request Body**
```json
{
  "url": "https://example.com",
  "active": true
}
```

**Response**
```json
{
  "success": true,
  "tab": {
    "id": 123,
    "url": "https://example.com",
    "title": "Example Domain"
  },
  "requestId": "uuid"
}
```

#### GET /tabs

List all open tabs.

**Response**
```json
{
  "success": true,
  "tabs": [
    {
      "id": 123,
      "url": "https://example.com",
      "title": "Example Domain",
      "active": true,
      "windowId": 1
    }
  ]
}
```

#### GET /tab/{tab_id}/content

Get page content.

**Response**
```json
{
  "success": true,
  "content": {
    "html": "<!DOCTYPE html>...",
    "text": "Page text content",
    "title": "Page Title",
    "url": "https://example.com"
  }
}
```

#### POST /tab/{tab_id}/interact

Interact with page elements.

**Request Body**
```json
{
  "action": "click",
  "selector": "#button-id",
  "value": "optional value",
  "timeout": 5000
}
```

**Actions**

| Action | Description | Required Fields |
|--------|-------------|----------------|
| `click` | Click element | `selector` |
| `input` | Type text | `selector`, `value` |
| `select` | Select option | `selector`, `value` |
| `wait` | Wait milliseconds | `timeout` |
| `waitForElement` | Wait for element | `selector`, `timeout` |
| `getText` | Get text content | `selector` |
| `getAttribute` | Get attribute | `selector`, `value` (attr name) |

**Response**
```json
{
  "success": true,
  "result": {
    "success": true,
    "action": "click",
    "selector": "#button-id"
  }
}
```

#### DELETE /tab/{tab_id}

Close a tab.

**Response**
```json
{
  "success": true,
  "requestId": "uuid"
}
```

---

## Error Responses

### 503 Service Unavailable

Extension not connected.

```json
{
  "detail": "Chrome extension not connected. Please ensure the extension is installed and running."
}
```

### 504 Gateway Timeout

Extension didn't respond in time.

```json
{
  "detail": "Extension did not respond within 30 seconds"
}
```

### 500 Internal Server Error

Error from extension.

```json
{
  "detail": "Element not found: #button-id"
}
```

---

## WebSocket

### ws://localhost:8000/ws

WebSocket endpoint for extension connection. Not intended for direct client use.

**Message Format**
```json
{
  "action": "createTab",
  "url": "https://example.com",
  "requestId": "uuid"
}
```
