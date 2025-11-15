# Troubleshooting Guide

## Extension Disconnecting

**Issue:** Extension shows "✗ Chrome extension disconnected" in server logs

**Why it happens:**
Chrome service workers automatically sleep after 30 seconds of inactivity to save resources. This is normal Chrome behavior.

**Solutions implemented:**

1. **Heartbeat mechanism** - Extension sends ping every 30 seconds to keep connection alive
2. **Keep-alive interval** - Service worker stays active with periodic checks
3. **Auto-reconnect** - Extension automatically reconnects if disconnected

**What you should see:**
- Extension connects on startup
- Stays connected during operations
- May briefly disconnect when idle (will auto-reconnect)
- All API calls work regardless of connection status

## Extension Not Connecting

**Symptoms:**
- API returns "503 Service Unavailable"
- Server shows "extension_connected: false"

**Solutions:**

1. **Reload extension:**
   - Go to `chrome://extensions/`
   - Click refresh icon on "Chrome Automation API"
   - Check service worker console for "✓ Connected"

2. **Check server is running:**
   ```bash
   # Should show server running
   curl http://localhost:8000
   ```

3. **Check WebSocket URL:**
   - Extension connects to `ws://localhost:8000/ws`
   - Make sure port 8000 is not blocked

4. **Check extension console:**
   - Click "service worker" link in chrome://extensions/
   - Look for connection errors

## Port Already in Use

**Error:** `[Errno 10048] error while attempting to bind on address`

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <process_id> /F

# Or change port in .env
PORT=8001
```

## API Timeout

**Error:** "Extension did not respond within 30 seconds"

**Causes:**
- Page taking too long to load
- Element not found
- Network issues

**Solutions:**

1. Increase timeout in `.env`:
   ```
   EXTENSION_RESPONSE_TIMEOUT=60
   ```

2. Use `waitForElement` before interacting:
   ```python
   requests.post(f"{API_BASE}/tab/{tab_id}/interact", json={
       "action": "waitForElement",
       "selector": "#button",
       "timeout": 10000
   })
   ```

## Element Not Found

**Error:** "Element not found: #selector"

**Solutions:**

1. **Wait for page load:**
   ```python
   time.sleep(2)  # Wait for page to load
   ```

2. **Use correct selector:**
   - Inspect element in Chrome DevTools
   - Copy selector (right-click → Copy → Copy selector)

3. **Try multiple selectors:**
   ```python
   selectors = ['#button', '.btn', 'button[type="submit"]']
   for selector in selectors:
       try:
           response = requests.post(...)
           if response.ok:
               break
       except:
           continue
   ```

## Server Won't Start

**Error:** Module not found or import errors

**Solution:**
```bash
# Reinstall dependencies
uv pip install -r requirements.txt

# Or use install.bat
install.bat
```

## Extension Permissions

**Issue:** Extension can't access certain sites

**Solution:**
The extension has `<all_urls>` permission. If blocked:
1. Check Chrome settings → Privacy and security → Site Settings
2. Ensure extension has permission for the site
3. Some sites (chrome://, chrome-extension://) are restricted by Chrome

## WebSocket Connection Failed

**Error:** "WebSocket error" in extension console

**Solutions:**

1. **Check server is running:**
   ```bash
   curl http://localhost:8000
   ```

2. **Check firewall:**
   - Allow port 8000 in Windows Firewall
   - Or disable firewall temporarily for testing

3. **Check antivirus:**
   - Some antivirus software blocks WebSocket connections
   - Add exception for localhost:8000

## Getting Help

If issues persist:

1. **Check server logs:**
   - Look at terminal running `start.bat`
   - Check for error messages

2. **Check extension console:**
   - Go to `chrome://extensions/`
   - Click "service worker"
   - Look for errors

3. **Enable debug mode:**
   - Set `DEBUG=True` in `.env`
   - Restart server
   - More detailed logs will appear

4. **Test basic connectivity:**
   ```bash
   uv run python check_connection.py
   ```
