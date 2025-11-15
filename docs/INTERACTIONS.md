# Browser Interactions Guide

Complete guide for interacting with web page elements using the Browser Automation API.

## Overview

The `/tab/{tab_id}/interact` endpoint allows you to perform various interactions with web page elements including clicking buttons, filling forms, selecting dropdowns, and extracting data.

---

## Endpoint

```
POST /tab/{tab_id}/interact
```

**Path Parameters:**
- `tab_id` (integer): The ID of the tab to interact with

**Request Body:**
```json
{
  "action": "click",
  "selector": "#button-id",
  "value": "optional value",
  "timeout": 5000
}
```

---

## Supported Actions

### 1. Click Elements

Click any clickable element (buttons, links, etc.)

**Request:**
```json
{
  "action": "click",
  "selector": "#submit-button"
}
```

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

**Features:**
- Automatically scrolls element into view
- Waits briefly before clicking for stability
- Returns element details

---

### 2. Input Text

Fill input fields, textareas, and contenteditable elements

**Request:**
```json
{
  "action": "input",
  "selector": "input[name='username']",
  "value": "john_doe"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "action": "input",
    "selector": "input[name='username']",
    "value": "john_doe",
    "elementTag": "INPUT",
    "elementType": "text"
  }
}
```

**Features:**
- Automatically focuses the element
- Clears existing value
- Triggers input, change, and keyboard events
- Works with React, Vue, Angular forms

---

### 3. Select Dropdown Options

Select an option from a `<select>` dropdown

**Request:**
```json
{
  "action": "select",
  "selector": "#country-select",
  "value": "USA"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "action": "select",
    "selector": "#country-select",
    "value": "USA"
  }
}
```

---

### 4. Get Text Content

Extract text content from any element

**Request:**
```json
{
  "action": "getText",
  "selector": "h1.title"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "action": "getText",
    "selector": "h1.title",
    "text": "Welcome to Our Website"
  }
}
```

---

### 5. Get Attribute Value

Get any attribute value from an element

**Request:**
```json
{
  "action": "getAttribute",
  "selector": "a.download-link",
  "value": "href"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "action": "getAttribute",
    "selector": "a.download-link",
    "attribute": "href",
    "value": "https://example.com/file.pdf"
  }
}
```

**Common Attributes:**
- `href` - Link URLs
- `src` - Image/script sources
- `data-*` - Custom data attributes
- `class` - CSS classes
- `id` - Element ID
- `value` - Input values

---

### 6. Wait for Element

Wait for an element to appear in the DOM

**Request:**
```json
{
  "action": "waitForElement",
  "selector": ".loading-complete",
  "timeout": 10000
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "action": "waitForElement",
    "selector": ".loading-complete"
  }
}
```

**Use Cases:**
- Wait for dynamic content to load
- Wait for AJAX requests to complete
- Wait for animations to finish

---

### 7. Find Element

Find an element and get detailed information about it

**Request:**
```json
{
  "action": "findElement",
  "selector": "#my-button"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "action": "findElement",
    "selector": "#my-button",
    "found": true,
    "element": {
      "tag": "BUTTON",
      "id": "my-button",
      "className": "btn btn-primary",
      "text": "Click Me",
      "visible": true,
      "position": {
        "x": 100,
        "y": 200,
        "width": 120,
        "height": 40
      }
    }
  }
}
```

**Use Cases:**
- Verify element exists before interacting
- Check if element is visible
- Get element position and size
- Debug selector issues

---

### 8. Wait (Delay)

Simple delay/wait for a specified duration

**Request:**
```json
{
  "action": "wait",
  "timeout": 2000
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "action": "wait",
    "duration": 2000
  }
}
```

---

## CSS Selectors Guide

### By ID
```css
#element-id
button#submit-btn
```

### By Class
```css
.class-name
button.btn-primary
.container .button
```

### By Attribute
```css
[name="username"]
[data-action="submit"]
[type="text"]
input[placeholder="Search"]
```

### By Tag
```css
button
input
textarea
a
```

### Combinators
```css
/* Direct child */
div > button

/* Descendant */
div button

/* Adjacent sibling */
h1 + p

/* General sibling */
h1 ~ p
```

### Pseudo-classes
```css
button:first-child
input:nth-child(2)
a:last-of-type
div:not(.excluded)
```

### Complex Selectors
```css
/* Multiple conditions */
button.submit[type="submit"]

/* Multiple selectors */
button, input[type="submit"]

/* Nested */
div.form-container > form > button.submit
```

---

## Common Use Cases

### Login Form
```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

# Fill username
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "input",
    "selector": "#username",
    "value": "user@example.com"
})

# Fill password
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "input",
    "selector": "#password",
    "value": "secure_password"
})

# Click login button
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": "button[type='submit']"
})
```

### Search and Extract Results
```python
import requests
import time

BASE_URL = "http://localhost:8000"
tab_id = 123456789

# Fill search box
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "input",
    "selector": "input[name='q']",
    "value": "Python automation"
})

# Click search
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": "button.search-btn"
})

# Wait for results
time.sleep(2)
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "waitForElement",
    "selector": ".results",
    "timeout": 5000
})

# Get first result text
response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "getText",
    "selector": ".result:first-child h3"
})
print(response.json()["result"]["text"])
```

### Form with Dropdown
```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

# Fill name
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "input",
    "selector": "#name",
    "value": "John Doe"
})

# Select country
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "select",
    "selector": "#country",
    "value": "USA"
})

# Select age range
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "select",
    "selector": "select[name='age']",
    "value": "25-34"
})

# Submit
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": "button[type='submit']"
})
```

### Extract Data from Table
```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

# Get all table rows
rows = []
for i in range(1, 11):  # First 10 rows
    response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
        "action": "getText",
        "selector": f"table tr:nth-child({i})"
    })
    
    if response.json().get("success"):
        rows.append(response.json()["result"]["text"])

print("Table data:", rows)
```

### Click Button by Text Content
```python
import requests

BASE_URL = "http://localhost:8000"
tab_id = 123456789

# Find button containing specific text
response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": "button:contains('Submit')"
})

# Alternative: Use XPath-like approach with findElement first
# Then click by ID or class
```

---

## Error Handling

### Element Not Found
```json
{
  "success": false,
  "error": "Element not found: #non-existent"
}
```

**Solutions:**
- Verify the selector is correct
- Check if element is in an iframe
- Wait for element to load with `waitForElement`
- Use browser DevTools to test selector

### Timeout
```json
{
  "success": false,
  "error": "Timeout waiting for element: .slow-loader"
}
```

**Solutions:**
- Increase timeout value
- Check if element actually appears
- Verify page is fully loaded

### Element Not Interactable
```json
{
  "success": false,
  "error": "Element is not interactable"
}
```

**Solutions:**
- Element might be hidden or covered
- Wait for animations to complete
- Scroll element into view (automatic for click)
- Check if element is disabled

---

## Best Practices

### 1. Use Specific Selectors
```python
# ❌ Too generic
selector = "button"

# ✓ Specific and reliable
selector = "button#submit-form"
selector = "button[data-testid='submit']"
```

### 2. Wait for Dynamic Content
```python
# ❌ Immediate interaction
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": ".dynamic-button"
})

# ✓ Wait for element first
requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "waitForElement",
    "selector": ".dynamic-button",
    "timeout": 5000
})

requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "click",
    "selector": ".dynamic-button"
})
```

### 3. Verify Before Interacting
```python
# Check if element exists and is visible
response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
    "action": "findElement",
    "selector": "#submit-btn"
})

if response.json()["result"]["found"]:
    # Element exists, proceed with interaction
    requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
        "action": "click",
        "selector": "#submit-btn"
    })
```

### 4. Handle Errors Gracefully
```python
try:
    response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
        "action": "click",
        "selector": "#button"
    })
    
    result = response.json()
    if not result.get("success"):
        print(f"Error: {result.get('error')}")
        # Fallback logic here
        
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

---

## Troubleshooting

### Selector Not Working

1. **Test in Browser Console:**
   ```javascript
   document.querySelector("#your-selector")
   ```

2. **Use Browser DevTools:**
   - Right-click element → Inspect
   - Copy selector from Elements panel

3. **Try Alternative Selectors:**
   ```python
   # Try different approaches
   selectors = [
       "#element-id",
       ".element-class",
       "[data-id='element']",
       "button:nth-child(2)"
   ]
   ```

### Element in Shadow DOM

Shadow DOM elements require special handling:
```python
# Use pierce combinator (if supported)
selector = "custom-element >>> button"
```

### Element in Iframe

For iframe elements, you may need to:
1. Switch to iframe context
2. Interact with element
3. Switch back to main context

---

## Performance Tips

1. **Batch Operations:** Group multiple interactions together
2. **Minimize Waits:** Use `waitForElement` instead of fixed delays
3. **Reuse Tab IDs:** Keep tabs open for multiple operations
4. **Specific Selectors:** Faster than complex queries

---

## Related Documentation

- [API Reference](API.md)
- [Tab Management](TAB_MANAGEMENT.md)
- [Content Extraction](CONTENT_EXTRACTION.md)
- [Troubleshooting](TROUBLESHOOTING.md)
