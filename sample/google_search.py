"""
Google Search Automation Example
Searches for a query and returns results
"""

import requests
import time
import json

API_BASE = "http://localhost:8000"

def search_google(query: str) -> dict:
    """
    Search Google and return results
    
    Args:
        query: Search query string
        
    Returns:
        dict with search results
    """
    
    print(f"Searching Google for: {query}")
    
    # Step 1: Open Google
    print("\n1. Opening Google...")
    response = requests.post(f"{API_BASE}/tab/new", json={
        "url": "https://www.google.com",
        "active": True
    })
    
    if not response.ok:
        return {"error": f"Failed to open tab: {response.text}"}
    
    tab_data = response.json()
    tab_id = tab_data["tab"]["id"]
    print(f"   ✓ Tab opened (ID: {tab_id})")
    
    # Wait for page to load
    time.sleep(2)
    
    # Step 2: Find and fill search box
    print("\n2. Entering search query...")
    
    # Try different selectors for Google search box
    selectors = [
        'textarea[name="q"]',
        'input[name="q"]',
        'textarea[title="Search"]',
        'input[title="Search"]'
    ]
    
    search_success = False
    for selector in selectors:
        try:
            response = requests.post(
                f"{API_BASE}/tab/{tab_id}/interact",
                json={
                    "action": "input",
                    "selector": selector,
                    "value": query
                }
            )
            
            if response.ok and response.json().get("success"):
                print(f"   ✓ Query entered using selector: {selector}")
                search_success = True
                break
        except:
            continue
    
    if not search_success:
        return {"error": "Could not find search box"}
    
    time.sleep(1)
    
    # Step 3: Submit search (press Enter by clicking search button or form submit)
    print("\n3. Submitting search...")
    
    # Try to click search button
    button_selectors = [
        'input[name="btnK"]',
        'button[type="submit"]',
        'input[type="submit"]'
    ]
    
    for selector in button_selectors:
        try:
            response = requests.post(
                f"{API_BASE}/tab/{tab_id}/interact",
                json={
                    "action": "click",
                    "selector": selector
                }
            )
            
            if response.ok and response.json().get("success"):
                print(f"   ✓ Search submitted")
                break
        except:
            continue
    
    # Wait for results to load
    print("\n4. Waiting for results...")
    time.sleep(3)
    
    # Step 4: Get page content
    print("\n5. Extracting results...")
    response = requests.get(f"{API_BASE}/tab/{tab_id}/content")
    
    if not response.ok:
        return {"error": f"Failed to get content: {response.text}"}
    
    content_data = response.json()
    page_content = content_data["content"]
    
    # Extract useful information
    results = {
        "query": query,
        "url": page_content.get("url", ""),
        "title": page_content.get("title", ""),
        "text_content": page_content.get("text", "")[:2000],  # First 2000 chars
        "html_length": len(page_content.get("html", "")),
        "tab_id": tab_id
    }
    
    print(f"   ✓ Results extracted")
    print(f"   - URL: {results['url']}")
    print(f"   - Title: {results['title']}")
    print(f"   - Content length: {results['html_length']} bytes")
    
    # Step 5: Close tab (optional)
    print("\n6. Closing tab...")
    requests.delete(f"{API_BASE}/tab/{tab_id}")
    print("   ✓ Tab closed")
    
    return results

def main():
    """Main execution"""
    
    print("="*70)
    print("Google Search Automation")
    print("="*70)
    
    # Check if server is running
    try:
        response = requests.get(API_BASE)
        server_info = response.json()
        
        if not server_info.get("extension_connected"):
            print("\n✗ Error: Chrome extension not connected!")
            print("  Make sure:")
            print("  1. Extension is loaded in Chrome")
            print("  2. Server is running (start.bat)")
            return
        
        print(f"\n✓ Server running: {server_info['name']} v{server_info['version']}")
        print(f"✓ Extension connected\n")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Server not running!")
        print("  Start the server with: start.bat")
        return
    
    # Perform search
    results = search_google("cyber24bd")
    
    # Display results
    print("\n" + "="*70)
    print("SEARCH RESULTS")
    print("="*70)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Save to file
    output_file = "sample/search_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to: {output_file}")

if __name__ == "__main__":
    main()
