# Extension Architecture

## Overview

The Chrome extension uses a modern modular architecture with ES6 modules for better maintainability and scalability.

## Module Structure

```
extension/
├── background-new.js          # Main entry point
├── manifest.json              # Extension configuration
└── modules/
    ├── connection.js          # WebSocket connection management
    ├── commands.js            # Command routing
    ├── tabs.js                # Tab operations
    ├── content.js             # Content extraction (HTML/Markdown)
    ├── interactions.js        # DOM interactions
    └── keepalive.js           # Service worker keep-alive
```

## Modules

### 1. ConnectionManager (`connection.js`)

Manages WebSocket connection with the server.

**Features:**
- Auto-reconnect on disconnect
- Heartbeat mechanism (ping/pong)
- Message routing
- Connection state management

**Methods:**
- `connect()` - Establish WebSocket connection
- `send(data)` - Send message to server
- `setMessageHandler(handler)` - Set message callback
- `isConnected()` - Check connection status

### 2. CommandHandler (`commands.js`)

Routes incoming commands to appropriate modules.

**Supported Commands:**
- `createTab` - Create new tab
- `getTabs` - List all tabs
- `closeTab` - Close tab
- `getContent` - Get page content (HTML/Markdown)
- `getMetadata` - Get page metadata
- `interact` - Interact with page elements

**Methods:**
- `handle(message)` - Process command and return result

### 3. TabManager (`tabs.js`)

Handles tab lifecycle operations.

**Methods:**
- `createTab(url, active)` - Create and wait for tab load
- `getTabs()` - Get all open tabs
- `closeTab(tabId)` - Close specific tab
- `waitForTabLoad(tabId, timeout)` - Wait for tab to finish loading

### 4. ContentExtractor (`content.js`)

Extracts page content in multiple formats.

**Features:**
- HTML extraction
- Markdown conversion (using Turndown.js CDN)
- Metadata extraction (title, description, keywords, Open Graph)

**Methods:**
- `getContent(tabId, format)` - Get content in 'html' or 'markdown' format
- `getPageMetadata(tabId)` - Extract page metadata

**Markdown Conversion:**
- Dynamically loads Turndown.js from CDN
- Converts HTML to clean Markdown
- Preserves headings, links, lists, code blocks
- Fallback to plain text if library fails

### 5. InteractionManager (`interactions.js`)

Handles DOM interactions in page context.

**Supported Actions:**
- `click` - Click element
- `input` - Type into input field
- `select` - Select dropdown option
- `wait` - Wait for milliseconds
- `waitForElement` - Wait for element to appear
- `getText` - Extract text content
- `getAttribute` - Get element attribute

**Methods:**
- `interact(tabId, interaction)` - Execute interaction

### 6. KeepAliveManager (`keepalive.js`)

Prevents Chrome service worker from sleeping.

**Features:**
- Periodic ping to keep worker active
- Configurable interval (default: 20s)

**Methods:**
- `start()` - Start keep-alive timer
- `stop()` - Stop keep-alive timer

## Data Flow

```
Server Request
    ↓
WebSocket Message
    ↓
ConnectionManager
    ↓
CommandHandler
    ↓
Specific Module (TabManager, ContentExtractor, etc.)
    ↓
Chrome API / Page Injection
    ↓
Result
    ↓
ConnectionManager
    ↓
WebSocket Response
    ↓
Server
```

## Content Extraction Flow

### HTML Format

```
Request: GET /tab/{id}/content?format=html
    ↓
ContentExtractor.getContent(tabId, 'html')
    ↓
Inject extractPageContent('html')
    ↓
Return: {
  url, title, html, text, format: 'html'
}
```

### Markdown Format

```
Request: GET /tab/{id}/content?format=markdown
    ↓
ContentExtractor.getContent(tabId, 'markdown')
    ↓
Inject extractPageContent('markdown')
    ↓
Load Turndown.js from CDN (if not loaded)
    ↓
Convert HTML → Markdown
    ↓
Return: {
  url, title, markdown, format: 'markdown'
}
```

### Metadata Extraction

```
Request: GET /tab/{id}/metadata
    ↓
ContentExtractor.getPageMetadata(tabId)
    ↓
Inject extractMetadata()
    ↓
Parse <meta> tags, Open Graph tags
    ↓
Return: {
  url, title, description, keywords, author, ogTitle, ogDescription
}
```

## Error Handling

Each module implements try-catch error handling:

```javascript
try {
  // Operation
  return { success: true, data: result };
} catch (error) {
  throw new Error(`Failed to ...: ${error.message}`);
}
```

Errors are caught by CommandHandler and returned as:

```javascript
{
  success: false,
  error: "Error message",
  requestId: "uuid"
}
```

## Configuration

Configuration is centralized in `background-new.js`:

```javascript
const CONFIG = {
  wsUrl: 'ws://localhost:8000/ws',
  reconnectDelay: 5000,           // 5 seconds
  heartbeatInterval: 30000,       // 30 seconds
  keepAliveInterval: 20000        // 20 seconds
};
```

## Extension Lifecycle

1. **Installation/Startup:**
   - Initialize modules
   - Start keep-alive manager
   - Connect to WebSocket server

2. **Runtime:**
   - Maintain WebSocket connection
   - Handle incoming commands
   - Execute operations
   - Return results

3. **Idle:**
   - Keep-alive prevents sleep
   - Heartbeat maintains connection
   - Auto-reconnect if disconnected

## Adding New Features

### 1. Create New Module

```javascript
// extension/modules/myfeature.js
export class MyFeature {
  async doSomething(param) {
    // Implementation
    return { success: true, result: data };
  }
}
```

### 2. Register in CommandHandler

```javascript
// extension/modules/commands.js
import { MyFeature } from './myfeature.js';

export class CommandHandler {
  constructor() {
    this.myFeature = new MyFeature();
  }
  
  async handle(message) {
    switch (action) {
      case 'myAction':
        result = await this.myFeature.doSomething(message.param);
        break;
    }
  }
}
```

### 3. Add Server Endpoint

```python
# app/routes/tabs.py
@router.post("/{tab_id}/myaction")
async def my_action(tab_id: int, param: str):
    response = await extension_service.send_command({
        "action": "myAction",
        "tabId": tab_id,
        "param": param
    })
    return response
```

## Best Practices

1. **Modularity:** Each module has single responsibility
2. **Error Handling:** Always wrap operations in try-catch
3. **Async/Await:** Use async/await for all Chrome API calls
4. **Type Safety:** Document parameters and return types
5. **Logging:** Use console.log for debugging
6. **Cleanup:** Remove event listeners when done
7. **Timeouts:** Always set timeouts for async operations

## Performance

- **Service Worker:** Stays active with keep-alive
- **WebSocket:** Single persistent connection
- **Lazy Loading:** Turndown.js loaded only when needed
- **Efficient Injection:** Minimal code injected into pages
- **Memory:** Modules are singletons, no duplication

## Security

- **Content Security:** Scripts injected only when needed
- **Permissions:** Minimal required permissions
- **Validation:** All inputs validated before execution
- **Error Messages:** No sensitive data in error messages
