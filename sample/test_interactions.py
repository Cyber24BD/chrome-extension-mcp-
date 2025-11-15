"""
Test script for browser interaction features
Demonstrates clicking buttons and filling inputs
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_interactions():
    print("=" * 60)
    print("BROWSER INTERACTION TEST")
    print("=" * 60)
    print()
    
    # Step 1: Create a test page
    print("Step 1: Creating new tab with Google...")
    response = requests.post(f"{BASE_URL}/tab/new", json={
        "url": "https://www.google.com",
        "active": True
    })
    
    if not response.json().get("success"):
        print("❌ Failed to create tab")
        return
    
    tab_id = response.json()["tab"]["id"]
    print(f"✓ Tab created: {tab_id}")
    print()
    
    # Wait for page to load
    time.sleep(3)
    
    # Step 2: Find the search input
    print("Step 2: Finding search input element...")
    response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
        "action": "findElement",
        "selector": "textarea[name='q']"
    })
    
    result = response.json()
    if result.get("success") and result.get("result", {}).get("found"):
        element = result["result"]["element"]
        print(f"✓ Element found:")
        print(f"  - Tag: {element['tag']}")
        print(f"  - Visible: {element['visible']}")
        print(f"  - Position: {element['position']}")
    else:
        print("❌ Element not found")
    print()
    
    # Step 3: Fill the search input
    print("Step 3: Filling search input with text...")
    response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
        "action": "input",
        "selector": "textarea[name='q']",
        "value": "Browser automation with Python"
    })
    
    result = response.json()
    if result.get("success"):
        print(f"✓ Input filled successfully")
        if result.get("result"):
            print(f"  - Element: {result['result'].get('elementTag')}")
            print(f"  - Value: {result['result'].get('value')}")
    else:
        print(f"❌ Failed to fill input: {result.get('error')}")
    print()
    
    # Step 4: Click the search button
    print("Step 4: Clicking search button...")
    time.sleep(1)
    
    response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
        "action": "click",
        "selector": "input[name='btnK']"
    })
    
    result = response.json()
    if result.get("success"):
        print(f"✓ Button clicked successfully")
        if result.get("result"):
            print(f"  - Element: {result['result'].get('elementTag')}")
            print(f"  - Text: {result['result'].get('elementText', 'N/A')}")
    else:
        print(f"❌ Failed to click button: {result.get('error')}")
    print()
    
    # Step 5: Wait for results
    print("Step 5: Waiting for search results...")
    time.sleep(3)
    
    response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
        "action": "waitForElement",
        "selector": "#search",
        "timeout": 5000
    })
    
    if response.json().get("success"):
        print("✓ Search results loaded")
    else:
        print("❌ Timeout waiting for results")
    print()
    
    # Step 6: Get text from first result
    print("Step 6: Getting text from first result...")
    response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
        "action": "getText",
        "selector": "h3"
    })
    
    result = response.json()
    if result.get("success") and result.get("result"):
        text = result["result"].get("text", "")
        print(f"✓ First result title: {text[:100]}")
    else:
        print("❌ Failed to get text")
    print()
    
    # Step 7: Get URL from first link
    print("Step 7: Getting URL from first link...")
    response = requests.post(f"{BASE_URL}/tab/{tab_id}/interact", json={
        "action": "getAttribute",
        "selector": "a[href]",
        "value": "href"
    })
    
    result = response.json()
    if result.get("success") and result.get("result"):
        url = result["result"].get("value", "")
        print(f"✓ First link URL: {url[:80]}")
    else:
        print("❌ Failed to get attribute")
    print()
    
    print("=" * 60)
    print("TEST COMPLETED SUCCESSFULLY ✓")
    print("=" * 60)
    print()
    print("Supported Selectors:")
    print("  - By ID: #element-id")
    print("  - By Class: .class-name")
    print("  - By Name: [name='field-name']")
    print("  - By Attribute: [data-action='submit']")
    print("  - By Type: input[type='text']")
    print("  - Complex: div.container > button.submit")
    print()
    print(f"Tab ID: {tab_id} (use this for more interactions)")

if __name__ == "__main__":
    try:
        test_interactions()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
