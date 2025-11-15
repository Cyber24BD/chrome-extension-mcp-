# MCP Server Architecture

Modular architecture for the Browser Automation MCP Server.

## 📁 Folder Structure

```
mcp/
├── server.py                    # Main MCP server entry point
├── config.py                    # Configuration settings
├── requirements.txt             # Dependencies
├── README.md                    # User documentation
├── ARCHITECTURE.md              # This file
├── test_mcp.py                  # Test script
├── install.bat                  # Installation script
├── claude_desktop_config.example.json
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   └── api_client.py            # HTTP client for API calls
│
├── tools/                       # Tool definitions
│   ├── __init__.py
│   ├── tab_tools.py             # Tab management tools
│   ├── content_tools.py         # Content extraction tools
│   └── interaction_tools.py     # Browser interaction tools
│
└── handlers/                    # Tool execution handlers
    ├── __init__.py
    ├── tab_handlers.py          # Tab management handlers
    ├── content_handlers.py      # Content extraction handlers
    └── interaction_handlers.py  # Browser interaction handlers
```

## 🏗️ Architecture Overview

### 1. Server Layer (`server.py`)

Main entry point that:
- Creates MCP server instance
- Registers tool list handler
- Registers tool execution handler
- Manages server lifecycle

### 2. Configuration (`config.py`)

Centralized configuration:
- API base URL
- Timeout settings
- Server name and version
- Environment variables

### 3. Utils Layer (`utils/`)

Reusable utilities:
- **api_client.py**: HTTP client for browser automation API
  - Singleton pattern for client instance
  - Async HTTP operations
  - Error handling

### 4. Tools Layer (`tools/`)

Tool definitions (schemas):
- **tab_tools.py**: Tab management tool schemas
  - browser_create_tab
  - browser_list_tabs
  - browser_close_tab
  - browser_navigate
  - browser_activate_tab
  - browser_reload_tab

- **content_tools.py**: Content extraction tool schemas
  - browser_get_content
  - browser_get_metadata

- **interaction_tools.py**: Browser interaction tool schemas
  - browser_click
  - browser_input
  - browser_get_text
  - browser_wait_for_element
  - browser_find_element
  - browser_select_option
  - browser_get_attribute

### 5. Handlers Layer (`handlers/`)

Tool execution logic:
- **tab_handlers.py**: Implements tab management operations
- **content_handlers.py**: Implements content extraction
- **interaction_handlers.py**: Implements browser interactions

Each handler:
- Calls browser automation API
- Formats responses for Claude
- Handles errors gracefully
- Returns MCP TextContent

## 🔄 Request Flow

```
Claude Desktop
      ↓
  MCP Protocol
      ↓
server.py (handle_call_tool)
      ↓
handlers/__init__.py (route to handler)
      ↓
specific_handler.py (execute logic)
      ↓
utils/api_client.py (call API)
      ↓
Browser Automation API
      ↓
Chrome Extension
      ↓
Browser
```

## 🎯 Design Principles

### 1. Separation of Concerns
- Tools define WHAT (schemas)
- Handlers define HOW (implementation)
- Utils provide shared functionality

### 2. Modularity
- Each module has single responsibility
- Easy to add new tools
- Easy to modify existing tools

### 3. Maintainability
- Clear folder structure
- Consistent naming conventions
- Well-documented code

### 4. Extensibility
- Add new tool: Create schema + handler
- Modify tool: Update schema or handler
- No need to touch server.py

## 📝 Adding a New Tool

### Step 1: Define Tool Schema

Add to appropriate file in `tools/`:

```python
# tools/new_category_tools.py
import mcp.types as types

def get_new_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="browser_new_action",
            description="Description of what it does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param1"]
            }
        )
    ]
```

### Step 2: Create Handler

Add to appropriate file in `handlers/`:

```python
# handlers/new_category_handlers.py
import mcp.types as types
from ..utils import call_api

async def handle_new_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "browser_new_action":
        result = await call_api("POST", "/endpoint", json=arguments)
        
        if result.get("success"):
            return [types.TextContent(
                type="text",
                text=f"✓ Action completed"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed: {result.get('error')}"
            )]
```

### Step 3: Register Tool

Update `tools/__init__.py`:

```python
from .new_category_tools import get_new_tools

def get_all_tools():
    return [
        *get_tab_tools(),
        *get_content_tools(),
        *get_interaction_tools(),
        *get_new_tools()  # Add here
    ]
```

### Step 4: Register Handler

Update `handlers/__init__.py`:

```python
from .new_category_handlers import handle_new_tool

async def handle_tool(name: str, arguments: dict):
    # Add routing logic
    elif name == "browser_new_action":
        return await handle_new_tool(name, arguments)
```

## 🧪 Testing

### Unit Testing

Test individual components:

```python
# Test API client
from utils import call_api
result = await call_api("GET", "/health")

# Test handler
from handlers.tab_handlers import handle_tab_tool
result = await handle_tab_tool("browser_list_tabs", {})
```

### Integration Testing

Test full flow:

```bash
python test_mcp.py
```

### Manual Testing

Test with Claude Desktop:
1. Update config
2. Restart Claude
3. Try commands

## 🔧 Configuration

### Environment Variables

```bash
# API Configuration
export BROWSER_API_URL="http://localhost:8000"
export BROWSER_API_TIMEOUT="30.0"

# Logging
export LOG_LEVEL="INFO"
```

### Claude Desktop Config

```json
{
  "mcpServers": {
    "browser-automation": {
      "command": "python",
      "args": ["path/to/mcp/server.py"],
      "env": {
        "BROWSER_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

## 📊 Error Handling

### Levels

1. **API Client**: HTTP errors, timeouts
2. **Handlers**: Business logic errors
3. **Server**: MCP protocol errors

### Strategy

- Always return TextContent (never raise)
- Include helpful error messages
- Suggest solutions when possible

## 🚀 Performance

### Optimizations

1. **Connection Pooling**: Reuse HTTP client
2. **Async Operations**: Non-blocking I/O
3. **Lazy Loading**: Import modules as needed

### Monitoring

- Check API response times
- Monitor memory usage
- Log slow operations

## 🔐 Security

### Best Practices

1. **Input Validation**: Validate all arguments
2. **Error Messages**: Don't expose sensitive info
3. **API Access**: Only localhost by default
4. **Timeouts**: Prevent hanging requests

## 📚 Related Documentation

- [Main README](README.md) - User guide
- [API Documentation](../README.md) - Browser automation API
- [MCP Specification](https://modelcontextprotocol.io) - Protocol details

## 🤝 Contributing

When contributing:
1. Follow existing patterns
2. Add tests for new features
3. Update documentation
4. Keep modules focused

## 📝 Changelog

### v1.0.0 - Modular Architecture
- Separated tools, handlers, and utils
- Added 14 browser automation tools
- Comprehensive error handling
- Full documentation
