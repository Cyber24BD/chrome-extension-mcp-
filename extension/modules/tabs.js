/**
 * Tab Management Module
 * Handles tab operations
 */

export class TabManager {
  
  async createTab(url, active = true) {
    try {
      const tab = await chrome.tabs.create({ url, active });
      
      // Wait for tab to load
      await this.waitForTabLoad(tab.id);
      
      return {
        success: true,
        tab: {
          id: tab.id,
          url: tab.url,
          title: tab.title,
          active: tab.active,
          windowId: tab.windowId,
          index: tab.index
        }
      };
    } catch (error) {
      throw new Error(`Failed to create tab: ${error.message}`);
    }
  }
  
  async getTabs(filter = {}) {
    try {
      const tabs = await chrome.tabs.query(filter);
      return {
        success: true,
        count: tabs.length,
        tabs: tabs.map(tab => ({
          id: tab.id,
          url: tab.url,
          title: tab.title,
          active: tab.active,
          windowId: tab.windowId,
          index: tab.index,
          pinned: tab.pinned,
          status: tab.status,
          favIconUrl: tab.favIconUrl
        }))
      };
    } catch (error) {
      throw new Error(`Failed to get tabs: ${error.message}`);
    }
  }
  
  async getActiveTab() {
    try {
      const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tabs.length === 0) {
        throw new Error('No active tab found');
      }
      
      return {
        success: true,
        tab: {
          id: tabs[0].id,
          url: tabs[0].url,
          title: tabs[0].title,
          active: tabs[0].active,
          windowId: tabs[0].windowId,
          index: tabs[0].index
        }
      };
    } catch (error) {
      throw new Error(`Failed to get active tab: ${error.message}`);
    }
  }
  
  async navigateTab(tabId, url) {
    try {
      await chrome.tabs.update(tabId, { url });
      
      // Wait for navigation to complete
      await this.waitForTabLoad(tabId);
      
      // Get updated tab info
      const tab = await chrome.tabs.get(tabId);
      
      return {
        success: true,
        tab: {
          id: tab.id,
          url: tab.url,
          title: tab.title,
          active: tab.active
        }
      };
    } catch (error) {
      throw new Error(`Failed to navigate tab: ${error.message}`);
    }
  }
  
  async activateTab(tabId) {
    try {
      const tab = await chrome.tabs.update(tabId, { active: true });
      
      return {
        success: true,
        tab: {
          id: tab.id,
          url: tab.url,
          title: tab.title,
          active: tab.active
        }
      };
    } catch (error) {
      throw new Error(`Failed to activate tab: ${error.message}`);
    }
  }
  
  async closeTab(tabId) {
    try {
      await chrome.tabs.remove(tabId);
      return { success: true };
    } catch (error) {
      throw new Error(`Failed to close tab: ${error.message}`);
    }
  }
  
  async reloadTab(tabId, bypassCache = false) {
    try {
      await chrome.tabs.reload(tabId, { bypassCache });
      await this.waitForTabLoad(tabId);
      
      return { success: true };
    } catch (error) {
      throw new Error(`Failed to reload tab: ${error.message}`);
    }
  }
  
  async waitForTabLoad(tabId, timeout = 30000) {
    return new Promise((resolve) => {
      const listener = (updatedTabId, info) => {
        if (updatedTabId === tabId && info.status === 'complete') {
          chrome.tabs.onUpdated.removeListener(listener);
          resolve();
        }
      };
      
      chrome.tabs.onUpdated.addListener(listener);
      
      // Timeout
      setTimeout(() => {
        chrome.tabs.onUpdated.removeListener(listener);
        resolve();
      }, timeout);
    });
  }
}
