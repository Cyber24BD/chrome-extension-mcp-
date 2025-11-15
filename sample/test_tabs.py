"""
Tab Management Test
Demonstrates all tab management features
"""

import requests
import time
import json

API_BASE = "http://localhost:8000"

def test_tab_management():
    """Test all tab management features"""
    
    print("="*70)
    print("Tab Management Test")
    print("="*70)
    
    # Check connection
    response = requests.get(API_BASE)
    if not response.json().get("extension_connected"):
        print("\n✗ Extension not connected!")
        return
    
    print("\n✓ Extension connected\n")
    
    # 1. List all current tabs
    print("1. Listing all current tabs...")
    response = requests.get(f"{API_BASE}/tabs")
    tabs = response.json()
    
    tab_count = tabs.get('count', len(tabs.get('tabs', [])))
    print(f"   ✓ Found {tab_count} tabs:")
    for tab in tabs['tabs']:
        status_icon = "●" if tab['active'] else "○"
        print(f"     {status_icon} [{tab['id']}] {tab['title']}")
        print(f"        URL: {tab['url']}")
        status = tab.get('status', 'unknown')
        pinned = tab.get('pinned', False)
        print(f"        Status: {status}, Pinned: {pinned}")
    
    # 2. Get active tab
    print("\n2. Getting active tab...")
    try:
        response = requests.get(f"{API_BASE}/tab/active")
        if response.ok:
            active_tab = response.json().get('tab')
            if active_tab:
                print(f"   ✓ Active tab: {active_tab['title']}")
                print(f"     URL: {active_tab['url']}")
            else:
                print("   ⚠ Active tab endpoint not available (reload extension)")
        else:
            print("   ⚠ Active tab endpoint not available (reload extension)")
    except Exception as e:
        print(f"   ⚠ Active tab feature not available: {e}")
    
    # 3. Create new tabs
    print("\n3. Creating new tabs...")
    test_urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://jsonplaceholder.typicode.com"
    ]
    
    new_tabs = []
    for url in test_urls:
        response = requests.post(f"{API_BASE}/tab/new", json={
            "url": url,
            "active": False  # Open in background
        })
        tab = response.json()['tab']
        new_tabs.append(tab)
        print(f"   ✓ Created tab {tab['id']}: {url}")
    
    time.sleep(2)
    
    # 4. List tabs again
    print("\n4. Listing tabs after creation...")
    response = requests.get(f"{API_BASE}/tabs")
    tabs = response.json()
    tab_count = tabs.get('count', len(tabs.get('tabs', [])))
    print(f"   ✓ Now have {tab_count} tabs")
    
    # 5. Activate first new tab
    print(f"\n5. Activating tab {new_tabs[0]['id']}...")
    try:
        response = requests.post(f"{API_BASE}/tab/{new_tabs[0]['id']}/activate")
        if response.ok:
            print(f"   ✓ Activated: {new_tabs[0]['title']}")
        else:
            print("   ⚠ Activate feature not available (reload extension)")
    except Exception as e:
        print(f"   ⚠ Activate feature not available: {e}")
    
    time.sleep(1)
    
    # 6. Navigate second tab
    print(f"\n6. Navigating tab {new_tabs[1]['id']} to Google...")
    try:
        response = requests.post(
            f"{API_BASE}/tab/{new_tabs[1]['id']}/navigate",
            json={"url": "https://google.com"}
        )
        if response.ok:
            result = response.json()
            updated_tab = result.get('tab')
            if updated_tab:
                print(f"   ✓ Navigated to: {updated_tab['url']}")
                print(f"   ✓ New title: {updated_tab['title']}")
            else:
                print("   ⚠ Navigate feature not available (reload extension)")
        else:
            print("   ⚠ Navigate feature not available (reload extension)")
    except Exception as e:
        print(f"   ⚠ Navigate feature not available: {e}")
    
    time.sleep(2)
    
    # 7. Reload third tab
    print(f"\n7. Reloading tab {new_tabs[2]['id']}...")
    try:
        response = requests.post(f"{API_BASE}/tab/{new_tabs[2]['id']}/reload")
        if response.ok:
            print(f"   ✓ Tab reloaded")
        else:
            print("   ⚠ Reload feature not available (reload extension)")
    except Exception as e:
        print(f"   ⚠ Reload feature not available: {e}")
    
    time.sleep(1)
    
    # 8. Get only active tabs
    print("\n8. Getting only active tabs...")
    response = requests.get(f"{API_BASE}/tabs", params={"active": True})
    active_tabs = response.json()
    active_count = active_tabs.get('count', len(active_tabs.get('tabs', [])))
    print(f"   ✓ Found {active_count} active tab(s):")
    for tab in active_tabs['tabs']:
        print(f"     ● [{tab['id']}] {tab['title']}")
    
    # 9. Close new tabs
    print("\n9. Closing created tabs...")
    for tab in new_tabs:
        response = requests.delete(f"{API_BASE}/tab/{tab['id']}")
        print(f"   ✓ Closed tab {tab['id']}")
    
    # 10. Final tab count
    print("\n10. Final tab count...")
    response = requests.get(f"{API_BASE}/tabs")
    tabs = response.json()
    final_count = tabs.get('count', len(tabs.get('tabs', [])))
    print(f"   ✓ Back to {final_count} tabs")
    
    print("\n" + "="*70)
    print("Test Complete!")
    print("="*70)
    
    # Save results
    results = {
        "initial_tabs": final_count,
        "created_tabs": len(new_tabs),
        "test_urls": test_urls,
        "final_tabs": final_count
    }
    
    with open("sample/tab_test_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✓ Results saved to: sample/tab_test_results.json")

def demo_tab_filtering():
    """Demonstrate tab filtering"""
    
    print("\n" + "="*70)
    print("Tab Filtering Demo")
    print("="*70 + "\n")
    
    # Get all tabs
    all_tabs = requests.get(f"{API_BASE}/tabs").json()
    all_count = all_tabs.get('count', len(all_tabs.get('tabs', [])))
    print(f"All tabs: {all_count}")
    
    # Get active tabs only
    active_tabs = requests.get(f"{API_BASE}/tabs", params={"active": True}).json()
    active_count = active_tabs.get('count', len(active_tabs.get('tabs', [])))
    print(f"Active tabs: {active_count}")
    
    # Get current window tabs
    current_window = requests.get(f"{API_BASE}/tabs", params={"current_window": True}).json()
    window_count = current_window.get('count', len(current_window.get('tabs', [])))
    print(f"Current window tabs: {window_count}")

def demo_session_save():
    """Save and restore tab session"""
    
    print("\n" + "="*70)
    print("Session Save/Restore Demo")
    print("="*70 + "\n")
    
    # Get all tabs
    tabs = requests.get(f"{API_BASE}/tabs").json()['tabs']
    
    # Save session
    session = [{"url": tab['url'], "title": tab['title']} for tab in tabs]
    
    with open("sample/tab_session.json", 'w') as f:
        json.dump(session, f, indent=2)
    
    print(f"✓ Saved {len(session)} tabs to session")
    
    # Show what was saved
    print("\nSaved tabs:")
    for item in session:
        print(f"  - {item['title']}")
        print(f"    {item['url']}")

if __name__ == "__main__":
    test_tab_management()
    
    # Uncomment to run additional demos
    # demo_tab_filtering()
    # demo_session_save()
