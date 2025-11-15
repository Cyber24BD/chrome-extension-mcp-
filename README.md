# Browser Automation REST API + MCP Server

A production-ready Chrome extension, FastAPI server, and MCP server for browser automation via REST API. Control Chrome tabs, extract content, and automate browser interactions through simple HTTP requests. **Interact with Chrome without changing your default browser, no caching interference, and zero tracking of personal details.**

## 🚀 Features

### Core Features
- **Tab Management**: Create, list, navigate, activate, reload, and close tabs
- **Advanced Content Extraction**: Extract page content in HTML or Markdown format with Python-based conversion
  - Multiple conversion methods (html2text, markdownify)
  - Automatic HTML cleaning (removes ads, scripts, styles)
  - Rich metadata extraction (headings, links, images count)
- **Browser Interactions**: Click elements, fill forms, get text, wait for elements
  - Support for all CSS selectors (ID, class, attribute, complex)
  - Auto-scroll elements into view
  - Framework-compatible (React, Vue, Angular)
- **WebSocket Communication**: Real-time bidirectional communication with keep-alive
- **Production Ready**: Comprehensive error handling, logging, and documentation

### AI Integration (MCP Server)
- **Model Context Protocol Server**: Let AI assistants like Claude Desktop control your browser
- **14 Browser Tools**: Full automation capabilities for AI
- **Modular Architecture**: Easy to extend and maintain
- **Zero Configuration**: Works out of the box with Claude Desktop

### Privacy & Security
- ✓ **No Default Browser Change**: Use Chrome for automation without affecting your main browser
- ✓ **No Caching Interference**: Separate Chrome instance, no impact on your browsing
- ✓ **Zero Tracking**: No personal data collection or tracking
- ✓ **Local Only**: All processing happens on your machine
- ✓ **Open Source**: Full transparency, audit the code yourself

---


## 🌟 Key Highlights

- **🔒 Privacy-First Automation**: Interact with Chrome without changing your default browser, no caching interference, and zero tracking of personal details
- **🚀 Non-Intrusive Operation**: Works alongside your existing Chrome setup without modifying browser settings or user profiles
- **🛡️ Secure Automation**: All interactions are isolated and don't affect your browsing history, cookies, or personal data
- **⚡ Real-Time Control**: Instant browser automation through REST API while maintaining complete privacy and security

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Load Chrome extension
# Go to chrome://extensions/ → Enable Developer Mode → Load Unpacked → Select 'extension' folder

# 3. Start server
python main.py

# 4. Test it
curl http://localhost:8000/health

# 5. (Optional) Setup MCP for Claude Desktop
cd mcp
pip install -r requirements.txt
# Add to Claude Desktop config (see MCP section below)
```

**That's it!** Your browser automation API is ready. Visit http://localhost:8000/docs for interactive API documentation.

---

## 📁 Project Structure

```
browser-automation-api/
├── app/                          # FastAPI application
│   ├── __init__.py
│   ├── api.py                    # Main API router
│   ├── config.py                 # Configuration settings
│   ├── models.py                 # Pydantic models
│   ├── routes/                   # API route modules
│   │   ├── __init__.py
│   │   ├── tabs.py               # Tab management endpoints
│   │   └── websocket.py          # WebSocket connection
│   └── services/                 # Business logic
│       ├── __init__.py
│       └── extension.py          # Extension communication service
│
├── extension/                    # Chrome extension
│   ├── manifest.json             # Extension configuration
│   ├── background.js             # Main extension script
│   └── modules/                  # Modular ES6 components
│       ├── connection.js         # WebSocket connection manager
│       ├── tabs.js               # Tab operations
│       ├── content.js            # Content extraction
│       ├── interactions.js       # Browser interactions
│       ├── commands.js           # Command dispatcher
│       └── keepalive.js          # Connection keep-alive
│
├── sample/                       # Example scripts
│   ├── README.md                 # Sample usage guide
│   ├── extract_youcom.py         # Content extraction example
│   ├── google_search.py          # Tab automation example
│   ├── test_markdown.py          # Markdown conversion test
│   ├── test_tabs.py              # Tab management test
│   ├── test_interactions.py      # Interaction testing
│   └── test_advanced_markdown.py # Advanced markdown test
│
├── scripts/                      # Utility scripts
│   ├── install.bat               # Windows installation script
│   ├── start.bat                 # Windows server start script
│   ├── test_tabs.bat             # Tab testing script
│   ├── test_markdown.bat         # Markdown testing script
│   ├── test_interactions.bat     # Interaction testing script
│   ├── test_advanced_markdown.bat# Advanced markdown test
│   └── extract_youcom.bat        # Content extraction script
│
├── mcp/                          # MCP Server for AI assistants
│   ├── server.py                 # MCP server entry point
│   ├── config.py                 # Configuration
│   ├── requirements.txt          # MCP dependencies
│   ├── README.md                 # MCP documentation
│   ├── ARCHITECTURE.md           # MCP architecture guide
│   ├── test_mcp.py               # MCP test script
│   ├── install.bat               # MCP installation
│   ├── claude_desktop_config.example.json
│   ├── utils/                    # Utility modules
│   │   └── api_client.py         # HTTP client
│   ├── tools/                    # Tool definitions (14 tools)
│   │   ├── tab_tools.py          # Tab management tools
│   │   ├── content_tools.py      # Content extraction tools
│   │   └── interaction_tools.py  # Browser interaction tools
│   └── handlers/                 # Tool execution handlers
│       ├── tab_handlers.py       # Tab operations
│       ├── content_handlers.py   # Content extraction
│       └── interaction_handlers.py # Browser interactions
│
├── docs/                         # Documentation
│   ├── README.md                 # Documentation index
│   ├── API.md                    # API reference
│   ├── ARCHITECTURE.md           # System architecture
│   ├── TAB_MANAGEMENT.md         # Tab operations guide
│   ├── CONTENT_EXTRACTION.md     # Content extraction guide
│   ├── FEATURES.md               # Feature overview
│   └── TROUBLESHOOTING.md        # Common issues & solutions
│
├── main.py                       # FastAPI server entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── .gitignore                    # Git ignore rules
```

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Google Chrome browser
- pip (Python package manager)


### Recomemned 

> ```bash
> # Create virtual environment ( Recomemned )
> python -m venv browser-automation-env
> 
> # Activate virtual environment
> # Windows:
> browser-automation-env\Scripts\activate
> # macOS/Linux:
> source browser-automation-env/bin/activate
> ```



### Step 1: Install Python Dependencies

```bash
# Windows
scripts\install.bat

# Or manually
pip install -r requirements.txt
```

### Step 2: Load Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right corner)
3. Click "Load unpacked"
4. Select the `extension` folder from this project
5. Note the extension ID (you'll see it under the extension name)

### Step 3: Start the Server

```bash
# Windows
scripts\start.bat

# Or manually
python main.py
```

The server will start at `http://localhost:8000`

### Step 4: Verify Connection

1. Check server logs for "Extension connected" message
2. Visit `http://localhost:8000/health` - should return `{"status": "ok"}`
3. Visit `http://localhost:8000/docs` for interactive API documentation

---

## 📡 API Endpoints

### Health Check

#### `GET /health`
Check if the server is running.

**Response:**
```json
{
  "status": "ok"
}
```

---

### Tab Management

#### `POST /tabs/create`
Create a new tab with a URL.

**Request Body:**
```json
{
  "url": "https://example.com",
  "active": true
}
```

**Parameters:**
- `url` (string, required): URL to open
- `active` (boolean, optional): Whether to activate the tab (default: true)

**Response:**
```json
{
  "success": true,
  "tabId": 123456789,
  "url": "https://example.com"
}
```

---

#### `GET /tabs/list`
Get a list of all open tabs with details.

**Response:**
```json
{
  "success": true,
  "tabs": [
    {
      "id": 123456789,
      "url": "https://example.com",
      "title": "Example Domain",
      "active": true,
      "windowId": 987654321,
      "index": 0,
      "pinned": false,
      "status": "complete"
    }
  ],
  "count": 1
}
```

---

#### `POST /tabs/navigate`
Navigate a tab to a new URL.

**Request Body:**
```json
{
  "tabId": 123456789,
  "url": "https://google.com"
}
```

**Parameters:**
- `tabId` (integer, required): ID of the tab to navigate
- `url` (string, required): URL to navigate to

**Response:**
```json
{
  "success": true,
  "tabId": 123456789,
  "url": "https://google.com"
}
```

---

#### `POST /tabs/activate`
Activate (focus) a specific tab.

**Request Body:**
```json
{
  "tabId": 123456789
}
```

**Parameters:**
- `tabId` (integer, required): ID of the tab to activate

**Response:**
```json
{
  "success": true,
  "tabId": 123456789
}
```

---

#### `POST /tabs/reload`
Reload a tab's content.

**Request Body:**
```json
{
  "tabId": 123456789,
  "bypassCache": false
}
```

**Parameters:**
- `tabId` (integer, required): ID of the tab to reload
- `bypassCache` (boolean, optional): Whether to bypass cache (default: false)

**Response:**
```json
{
  "success": true,
  "tabId": 123456789
}
```

---

#### `POST /tabs/close`
Close a specific tab.

**Request Body:**
```json
{
  "tabId": 123456789
}
```

**Parameters:**
- `tabId` (integer, required): ID of the tab to close

**Response:**
```json
{
  "success": true,
  "tabId": 123456789
}
```

---

### Content Extraction

#### `GET /tab/{tab_id}/content`
Extract content from a tab in HTML or Markdown format with **advanced Python-based conversion**.

**Query Parameters:**
- `format` (string, optional): Output format - "html" or "markdown" (default: "html")
- `method` (string, optional): Markdown conversion method - "html2text", "markdownify", or "auto" (default: "html2text")
- `clean` (boolean, optional): Clean HTML before conversion - removes scripts, styles, ads (default: true)

**Markdown Conversion Methods:**

1. **html2text** (default) - Advanced conversion with excellent formatting
   - Preserves tables, code blocks, and lists perfectly
   - Configurable line wrapping and link styles
   - Best for complex content (Wikipedia, documentation, articles)

2. **markdownify** - Simple, clean conversion
   - Lightweight and fast
   - Good for basic content
   - Minimal but accurate formatting

3. **auto** - Automatic fallback
   - Tries html2text first
   - Falls back to markdownify if needed

**HTML Response:**
```json
{
  "success": true,
  "content": {
    "format": "html",
    "html": "<!DOCTYPE html>...",
    "bodyHtml": "<div>...</div>",
    "text": "Plain text content",
    "url": "https://example.com",
    "title": "Example Domain",
    "timestamp": "2025-11-15T10:30:00.000Z"
  }
}
```

**Markdown Response:**
```json
{
  "success": true,
  "content": {
    "format": "markdown",
    "markdown": "# Example Domain\n\nThis domain is for use...",
    "url": "https://example.com",
    "title": "Example Domain",
    "timestamp": "2025-11-15T10:30:00.000Z",
    "conversion": {
      "method": "html2text",
      "length": 1234,
      "lines": 45,
      "metadata": {
        "headings": 5,
        "paragraphs": 12,
        "links": 8,
        "images": 3,
        "tables": 1,
        "lists": 4
      }
    }
  }
}
```

**Features:**
- ✓ Automatic HTML cleaning (removes scripts, styles, ads, popups)
- ✓ Preserves tables, code blocks, and formatting
- ✓ Extracts metadata (headings, links, images count)
- ✓ Post-processing for clean, readable output
- ✓ Multiple conversion methods for different use cases

---

### Browser Interactions

#### `POST /tab/{tab_id}/interact`
Interact with elements on the page (click, input, select, etc.).

**Request Body:**
```json
{
  "action": "click",
  "selector": "#submit-button"
}
```

**Parameters:**
- `tab_id` (integer, required): ID of the tab (in URL path)
- `action` (string, required): Type of interaction
- `selector` (string, required): CSS selector of element
- `value` (string, optional): Value for input/select actions
- `timeout` (integer, optional): Timeout in milliseconds (default: 5000)

**Supported Actions:**

1. **click** - Click an element
   ```json
   {
     "action": "click",
     "selector": "#button-id"
   }
   ```

2. **input** - Type text into an input field
   ```json
   {
     "action": "input",
     "selector": "input[name='search']",
     "value": "search query"
   }
   ```

3. **select** - Select an option from dropdown
   ```json
   {
     "action": "select",
     "selector": "#country-select",
     "value": "USA"
   }
   ```

4. **getText** - Get text content of an element
   ```json
   {
     "action": "getText",
     "selector": "h1"
   }
   ```

5. **getAttribute** - Get an attribute value
   ```json
   {
     "action": "getAttribute",
     "selector": "a.link",
     "value": "href"
   }
   ```

6. **waitForElement** - Wait for element to appear
   ```json
   {
     "action": "waitForElement",
     "selector": ".loading-complete",
     "timeout": 10000
   }
   ```

7. **findElement** - Find and get element details
   ```json
   {
     "action": "findElement",
     "selector": "#my-element"
   }
   ```

**CSS Selector Examples:**
- By ID: `#button-id` or `button#submit`
- By Class: `.btn-primary` or `button.submit-btn`
- By Attribute: `[data-action="submit"]` or `input[type="text"]`
- By Name: `input[name="username"]`
- Complex: `div.container > button.submit:first-child`

**Response:**
```json
{
  "success": true,
  "result": {
    "action": "click",
    "selector": "#submit-button",
    "elementTag": "BUTTON",
    "elementText": "Submit"
  }
}
```

---

### WebSocket

#### `WS /ws`
WebSocket endpoint for real-time bidirectional communication between server and extension.

**Connection URL:** `ws://localhost:8000/ws`

**Message Format:**
```json
{
  "command": "ping",
  "data": {}
}
```

---

## 💡 Usage Examples

### Python Examples

#### Create and Navigate Tabs

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a new tab
response = requests.post(f"{BASE_URL}/tabs/create", json={
    "url": "https://google.com",
    "active": True
})
tab_id = response.json()["tabId"]

# Navigate to a different URL
requests.post(f"{BASE_URL}/tabs/navigate", json={
    "tabId": tab_id,
    "url": "https://github.com"
})

# Close the tab
requests.post(f"{BASE_URL}/tabs/close", json={
    "tabId": tab_id
})
```

#### Extract Content as Markdown

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# Create tab
response = requests.post(f"{BASE_URL}/tab/new", json={
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "active": True
})
tab_id = response.json()["tab"]["id"]

# Wait for page to load
time.sleep(3)

# Extract as Markdown using html2text (best quality)
response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={
        "format": "markdown",
        "method": "html2text",
        "clean": True
    }
)

result = response.json()
markdown = result["content"]["markdown"]
metadata = result["content"]["conversion"]["metadata"]

print(f"Extracted {len(markdown)} characters")
print(f"Found: {metadata['headings']} headings, {metadata['links']} links")
print(markdown[:500])  # First 500 characters

# Save to file
with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown)
```

#### Compare Markdown Conversion Methods

```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

# Method 1: html2text (best for complex content)
response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={"format": "markdown", "method": "html2text"}
)
html2text_result = response.json()["content"]["markdown"]

# Method 2: markdownify (simple and clean)
response = requests.get(
    f"{BASE_URL}/tab/{tab_id}/content",
    params={"format": "markdown", "method": "markdownify"}
)
markdownify_result = response.json()["content"]["markdown"]

print(f"html2text: {len(html2text_result)} chars")
print(f"markdownify: {len(markdownify_result)} chars")
```

#### Browser Automation - Click & Input

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# Open Google
response = requests.post(f"{BASE_URL}/tab/new", json={
    "url": "https://google.com",
    "active": True
})
tab_id = response.json()["tab"]["id"]
time.sleep(2)

# Fill search box using input action
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "input",
    "selector": "textarea[name='q']",
    "value": "Python programming"
})

# Click search button by ID or selector
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": "input[name='btnK']"
})

# Wait for results to load
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "waitForElement",
    "selector": "#search",
    "timeout": 5000
})

# Get text from first result
response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "getText",
    "selector": "h3"
})
print(response.json()["result"]["text"])
```

#### Click Button by ID

```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789  # Your tab ID

# Click button by ID
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": "#submit-button"  # Using ID selector
})

# Click button by class
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": ".btn-primary"  # Using class selector
})

# Click button by data attribute
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": "[data-action='submit']"  # Using attribute selector
})
```

#### Fill Form with Multiple Inputs

```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

# Fill username
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "input",
    "selector": "#username",
    "value": "john_doe"
})

# Fill password
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "input",
    "selector": "input[type='password']",
    "value": "secure_password"
})

# Select country from dropdown
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "select",
    "selector": "#country",
    "value": "USA"
})

# Click submit button
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": "button[type='submit']"
})
```

### cURL Examples

#### Create Tab
```bash
curl -X POST http://localhost:8000/tabs/create \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "active": true}'
```

#### List Tabs
```bash
curl http://localhost:8000/tabs/list
```

#### Extract Content
```bash
curl -X POST http://localhost:8000/tabs/extract \
  -H "Content-Type: application/json" \
  -d '{"tabId": 123456789, "format": "markdown"}'
```

---

## � TMCP Server (AI Integration)

### What is MCP?

**Model Context Protocol (MCP)** allows AI assistants like Claude Desktop to use tools and interact with external systems. Our MCP server exposes all browser automation capabilities to AI assistants.

### Features

- **14 Browser Tools**: Complete browser automation for AI
- **Modular Architecture**: Separated tools, handlers, and utilities
- **Easy to Extend**: Add new tools without touching core code
- **Production Ready**: Comprehensive error handling and logging

### Available Tools

**Tab Management (6 tools):**
- `browser_create_tab` - Create new tabs
- `browser_list_tabs` - List all open tabs
- `browser_close_tab` - Close specific tabs
- `browser_navigate` - Navigate to URLs
- `browser_activate_tab` - Focus tabs
- `browser_reload_tab` - Reload tabs

**Content Extraction (2 tools):**
- `browser_get_content` - Extract as HTML/Markdown
- `browser_get_metadata` - Get page metadata

**Browser Interactions (7 tools):**
- `browser_click` - Click elements
- `browser_input` - Fill forms
- `browser_get_text` - Extract text
- `browser_wait_for_element` - Wait for elements
- `browser_find_element` - Find and verify elements
- `browser_select_option` - Select dropdowns
- `browser_get_attribute` - Get attributes

### Quick Setup

1. **Install MCP dependencies:**
   ```bash
   cd mcp
   pip install -r requirements.txt
   ```

2. **Configure Claude Desktop:**
   
   Add to your config file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

   ```json
   {
     "mcpServers": {
       "browser-automation": {
         "command": "python",
         "args": [
           "C:/path/to/your/project/mcp/server.py"
         ],
         "env": {}
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test it:**
   ```
   You: "List all open browser tabs"
   Claude: [Uses browser_list_tabs tool and shows results]
   ```

### Usage Examples with Claude

**Research and Summarize:**
```
You: "Go to Wikipedia, search for Python programming, and summarize the article"
Claude: [Creates tab, navigates, extracts content, summarizes]
```

**Fill Forms:**
```
You: "Go to example.com and fill out the contact form with my details"
Claude: [Opens page, fills form fields, submits]
```

**Compare Prices:**
```
You: "Compare laptop prices on Amazon and eBay"
Claude: [Opens both sites, searches, extracts prices, compares]
```

**Extract Data:**
```
You: "Get all article titles from the homepage"
Claude: [Extracts content, parses, lists titles]
```

### MCP Architecture

```
Claude Desktop
      ↓
  MCP Protocol
      ↓
  MCP Server (Modular)
  ├── Tools (Definitions)
  ├── Handlers (Logic)
  └── Utils (API Client)
      ↓
  Browser Automation API
      ↓
  Chrome Extension
      ↓
  Browser
```

### Documentation

- **[mcp/README.md](mcp/README.md)** - Complete MCP setup guide
- **[mcp/ARCHITECTURE.md](mcp/ARCHITECTURE.md)** - Architecture details
- **[mcp/test_mcp.py](mcp/test_mcp.py)** - Test script

---

## 🧪 Testing

Run the provided test scripts to verify functionality:

```bash
# Test tab management
scripts\test_tabs.bat

# Test markdown extraction
scripts\test_markdown.bat

# Test content extraction
scripts\extract_youcom.bat
```

Or run individual Python test scripts:

```bash
python sample/test_tabs.py
python sample/test_markdown.py
python sample/extract_youcom.py
python sample/google_search.py
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Settings
CORS_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL=INFO
```

### Extension Configuration

The extension connects automatically to `ws://localhost:8000/ws`. To change the server URL, edit `extension/modules/connection.js`:

```javascript
const WS_URL = 'ws://localhost:8000/ws';
```

---

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- **[API.md](docs/API.md)** - Complete API reference
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design
- **[TAB_MANAGEMENT.md](docs/TAB_MANAGEMENT.md)** - Tab operations guide
- **[CONTENT_EXTRACTION.md](docs/CONTENT_EXTRACTION.md)** - Content extraction guide
- **[MARKDOWN_CONVERSION.md](docs/MARKDOWN_CONVERSION.md)** - Advanced markdown conversion
- **[INTERACTIONS.md](docs/INTERACTIONS.md)** - Browser interactions guide
- **[FEATURES.md](docs/FEATURES.md)** - Feature overview
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### MCP Server Documentation

- **[mcp/README.md](mcp/README.md)** - Complete MCP setup and usage guide
- **[mcp/ARCHITECTURE.md](mcp/ARCHITECTURE.md)** - Modular architecture details

---

## 🆚 Why This Project?

### vs Other Browser Automation Tools

| Feature | This Project | Selenium | Puppeteer | Playwright |
|---------|-------------|----------|-----------|------------|
| **REST API** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **MCP Server (AI)** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **No Browser Change** | ✅ Yes | ⚠️ Separate | ⚠️ Separate | ⚠️ Separate |
| **Real-time WebSocket** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Advanced Markdown** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Zero Tracking** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Easy Setup** | ✅ Simple | ⚠️ Complex | ⚠️ Complex | ⚠️ Complex |
| **AI Integration** | ✅ Built-in | ❌ No | ❌ No | ❌ No |

### Key Advantages

1. **REST API First**: Simple HTTP requests, no complex drivers
2. **AI-Ready**: Built-in MCP server for Claude Desktop
3. **Privacy Focused**: No tracking, local processing only
4. **Production Ready**: Error handling, logging, documentation
5. **Modular Design**: Easy to extend and maintain
6. **Advanced Features**: Markdown conversion, metadata extraction
7. **Real Chrome**: Uses actual Chrome, not headless

---

## 🐛 Troubleshooting

### Extension Not Connecting

1. Check if the server is running: `http://localhost:8000/health`
2. Reload the extension in `chrome://extensions/`
3. Check browser console for errors (F12 → Console)
4. Verify WebSocket connection in server logs

### Commands Not Working

1. Ensure extension is connected (check server logs)
2. Verify tab ID is valid using `/tabs/list`
3. Check for JavaScript errors in browser console
4. Try reloading the target tab

### Content Extraction Returns Empty

1. Wait for page to fully load before extracting
2. Verify the CSS selector matches elements on the page
3. Check if the page uses dynamic content loading
4. Try extracting with default selector (body)

For more troubleshooting tips, see [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 🏗️ Architecture

### Communication Flow

```
HTTP Client → FastAPI Server → WebSocket → Chrome Extension → Browser
     ↓              ↓              ↓              ↓              ↓
  Request      Route Handler   Message      Command        Action
                                Queue      Dispatcher
```

### Key Components

1. **FastAPI Server**: Handles HTTP requests and WebSocket connections
2. **Chrome Extension**: Executes browser commands via Chrome APIs
3. **WebSocket**: Real-time bidirectional communication channel
4. **Command Queue**: Manages request/response matching
5. **Keep-Alive**: Maintains persistent connection

For detailed architecture information, see [ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is provided as-is for educational and development purposes.

---

## 🔗 Quick Links

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Chrome Extensions**: chrome://extensions/

---

## 📞 Support & Community

### Getting Help

1. **Documentation**: Check [docs/](docs/) folder for detailed guides
2. **Troubleshooting**: See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
3. **Issues**: [GitHub Issues](https://github.com/Cyber24BD/chrome-extension-mcp-/issues)
4. **Discussions**: [GitHub Discussions](https://github.com/Cyber24BD/chrome-extension-mcp-/discussions)

### Reporting Issues

When reporting issues, please include:
- Server logs
- Browser console errors
- Steps to reproduce
- Expected vs actual behavior

### Feature Requests

We welcome feature requests! Please:
1. Check existing issues first
2. Describe the use case
3. Explain why it's useful
4. Provide examples if possible

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Ways to Contribute

1. **Code**: Fix bugs, add features, improve performance
2. **Documentation**: Improve docs, add examples, fix typos
3. **Testing**: Report bugs, test new features
4. **Ideas**: Suggest improvements, new features

### Development Setup

```bash
# Clone repository
git clone https://github.com/Cyber24BD/chrome-extension-mcp-.git
cd chrome-extension-mcp-

# Install dependencies
pip install -r requirements.txt
cd mcp && pip install -r requirements.txt

# Run tests
python sample/test_tabs.py
python mcp/test_mcp.py
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow existing code patterns
- Add comments for complex logic
- Update documentation
- Add tests for new features

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=Cyber24BD/chrome-extension-mcp-&type=Date)](https://star-history.com/#Cyber24BD/chrome-extension-mcp-&Date)

---

## 🙏 Acknowledgments

- **FastAPI**: Modern web framework
- **Chrome Extensions API**: Browser automation capabilities
- **Model Context Protocol**: AI integration standard
- **html2text & markdownify**: Markdown conversion libraries
- **Community**: All contributors and users

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Cyber24BD/chrome-extension-mcp-?style=social)
![GitHub forks](https://img.shields.io/github/forks/Cyber24BD/chrome-extension-mcp-?style=social)
![GitHub issues](https://img.shields.io/github/issues/Cyber24BD/chrome-extension-mcp-)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Cyber24BD/chrome-extension-mcp-)
![License](https://img.shields.io/github/license/Cyber24BD/chrome-extension-mcp-)

---

**Happy Automating! 🚀**

Made with ❤️ by [Cyber24BD](https://github.com/Cyber24BD)
