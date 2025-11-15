# Browser Automation MCP Server

Model Context Protocol (MCP) server for browser automation. Allows AI assistants like Claude to control Chrome browser, navigate pages, extract content, and interact with web elements.

## 🚀 Features

- **Tab Management**: Create, list, navigate, and close browser tabs
- **Content Extraction**: Extract page content as HTML or Markdown
- **Page Interactions**: Click buttons, fill forms, get text
- **Wait Operations**: Wait for elements to appear
- **Advanced Markdown**: Python-based conversion with html2text/markdownify

## 📋 Prerequisites

1. **Browser Automation API Server** must be running
   ```bash
   # From project root
   python main.py
   ```

2. **Chrome Extension** must be loaded and connected
   - Load extension from `extension/` folder
   - Verify connection at http://localhost:8000/health

## 🛠️ Installation

### Step 1: Install Dependencies

```bash
cd mcp
pip install -r requirements.txt
```

Or install globally:
```bash
pip install mcp httpx
```

### Step 2: Configure in Claude Desktop

Add to your Claude Desktop configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "browser-automation": {
      "command": "python",
      "args": [
        "E:/Programming/Website Article/Chrome-Extention/mcp/server.py"
      ],
      "env": {}
    }
  }
}
```

**Important**: Replace the path with your actual project path!

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop to load the MCP server.

## 🔧 Available Tools

### 1. browser_create_tab
Create a new browser tab and navigate to a URL.

**Parameters:**
- `url` (string, required): URL to open
- `active` (boolean, optional): Make tab active (default: true)

**Example:**
```
Create a new tab and go to https://example.com
```

### 2. browser_list_tabs
Get a list of all open browser tabs.

**Example:**
```
Show me all open tabs
```

### 3. browser_close_tab
Close a specific browser tab.

**Parameters:**
- `tab_id` (integer, required): ID of tab to close

**Example:**
```
Close tab 123456789
```

### 4. browser_navigate
Navigate a tab to a new URL.

**Parameters:**
- `tab_id` (integer, required): ID of tab
- `url` (string, required): URL to navigate to

**Example:**
```
Navigate tab 123456789 to https://github.com
```

### 5. browser_get_content
Extract content from a tab in HTML or Markdown format.

**Parameters:**
- `tab_id` (integer, required): ID of tab
- `format` (string, optional): "html" or "markdown" (default: "markdown")
- `method` (string, optional): "html2text", "markdownify", or "auto" (default: "html2text")

**Example:**
```
Extract the content from tab 123456789 as markdown
```

### 6. browser_click
Click an element on the page using CSS selector.

**Parameters:**
- `tab_id` (integer, required): ID of tab
- `selector` (string, required): CSS selector (e.g., "#button-id", ".btn-class")

**Example:**
```
Click the submit button with id "submit-btn" on tab 123456789
```

### 7. browser_input
Fill an input field with text.

**Parameters:**
- `tab_id` (integer, required): ID of tab
- `selector` (string, required): CSS selector of input field
- `value` (string, required): Text to input

**Example:**
```
Fill the username field with "john_doe" on tab 123456789
```

### 8. browser_get_text
Get text content from an element.

**Parameters:**
- `tab_id` (integer, required): ID of tab
- `selector` (string, required): CSS selector

**Example:**
```
Get the text from the h1 element on tab 123456789
```

### 9. browser_wait_for_element
Wait for an element to appear on the page.

**Parameters:**
- `tab_id` (integer, required): ID of tab
- `selector` (string, required): CSS selector
- `timeout` (integer, optional): Timeout in milliseconds (default: 5000)

**Example:**
```
Wait for the loading spinner to disappear on tab 123456789
```

## 💡 Usage Examples

### Example 1: Research a Topic

```
User: Research Python programming on Wikipedia and summarize it

Claude will:
1. Create a new tab
2. Navigate to Wikipedia
3. Extract content as markdown
4. Summarize the content
```

### Example 2: Fill a Form

```
User: Go to example.com and fill out the contact form

Claude will:
1. Create a new tab with example.com
2. Fill input fields using CSS selectors
3. Click the submit button
```

### Example 3: Extract Data

```
User: Get all the article titles from the homepage

Claude will:
1. List open tabs or create new one
2. Extract content as markdown
3. Parse and list article titles
```

### Example 4: Multi-Tab Workflow

```
User: Compare prices on Amazon and eBay for "laptop"

Claude will:
1. Create tab for Amazon, search "laptop"
2. Extract prices
3. Create tab for eBay, search "laptop"
4. Extract prices
5. Compare and present results
```

## 🔍 CSS Selector Guide

### By ID
```css
#element-id
#submit-button
```

### By Class
```css
.class-name
.btn-primary
```

### By Attribute
```css
[name="username"]
[data-action="submit"]
input[type="text"]
```

### By Tag
```css
h1
button
input
```

### Complex Selectors
```css
div.container > button.submit
form input[name="email"]
.header .nav-item:first-child
```

## 🐛 Troubleshooting

### MCP Server Not Appearing in Claude

1. **Check configuration file path**
   - Verify the path in `claude_desktop_config.json` is correct
   - Use absolute path, not relative

2. **Check Python path**
   - Make sure `python` command works in terminal
   - Try using full Python path: `C:\Python312\python.exe`

3. **Restart Claude Desktop**
   - Completely close Claude Desktop
   - Reopen and check MCP servers

### Connection Errors

1. **API Server not running**
   ```bash
   # Start the API server
   python main.py
   ```

2. **Extension not connected**
   - Go to chrome://extensions/
   - Reload the Browser Automation extension
   - Check http://localhost:8000/health

3. **Port conflicts**
   - Make sure port 8000 is not in use
   - Check firewall settings

### Tool Execution Fails

1. **Invalid tab ID**
   - Use `browser_list_tabs` to get valid tab IDs
   - Tab IDs change when tabs are closed/reopened

2. **Element not found**
   - Verify CSS selector is correct
   - Use browser DevTools to test selector
   - Wait for page to load before interacting

3. **Timeout errors**
   - Increase timeout value
   - Check if page is loading slowly
   - Verify element actually appears

## 📚 Architecture

```
Claude Desktop
      ↓
   MCP Server (Python)
      ↓
   HTTP Requests
      ↓
FastAPI Server (localhost:8000)
      ↓
   WebSocket
      ↓
Chrome Extension
      ↓
   Chrome Browser
```

## 🔐 Security Notes

- MCP server runs locally on your machine
- Only accessible to Claude Desktop
- API server should only listen on localhost
- No external network access required
- All data stays on your computer

## 🚀 Advanced Usage

### Custom Configuration

Edit `server.py` to customize:
- API base URL (default: http://localhost:8000)
- Request timeout (default: 30 seconds)
- Tool descriptions and parameters

### Adding New Tools

1. Add tool definition in `handle_list_tools()`
2. Add tool handler in `handle_call_tool()`
3. Restart Claude Desktop

### Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

View MCP server logs in Claude Desktop:
- Help → View Logs → MCP Servers

## 📖 Related Documentation

- [Main API Documentation](../README.md)
- [Interaction Guide](../docs/INTERACTIONS.md)
- [Markdown Conversion](../docs/MARKDOWN_CONVERSION.md)
- [MCP Protocol Specification](https://modelcontextprotocol.io)

## 🤝 Contributing

To add new features:
1. Add tool to MCP server
2. Implement in FastAPI server if needed
3. Update documentation
4. Test with Claude Desktop

## 📄 License

Same as main project.

## 🆘 Support

For issues:
1. Check API server is running: http://localhost:8000/health
2. Check extension is connected
3. View Claude Desktop logs
4. Check MCP server logs

## 🎯 Quick Start Checklist

- [ ] API server running (`python main.py`)
- [ ] Chrome extension loaded and connected
- [ ] MCP dependencies installed (`pip install -r requirements.txt`)
- [ ] Claude Desktop config updated with correct path
- [ ] Claude Desktop restarted
- [ ] Test with: "List all open browser tabs"

---

**Happy Automating with Claude! 🚀**
