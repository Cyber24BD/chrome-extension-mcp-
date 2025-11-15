/**
 * Chrome Automation API - Background Service Worker
 * All-in-one file (no modules for compatibility)
 */

let ws = null;
let reconnectInterval = null;
let heartbeatInterval = null;
let keepAliveInterval = null;

const WS_URL = 'ws://localhost:8000/ws';
const RECONNECT_DELAY = 5000;
const HEARTBEAT_INTERVAL = 30000;
const KEEP_ALIVE_INTERVAL = 20000;

// WebSocket Connection
function connectWebSocket() {
  try {
    ws = new WebSocket(WS_URL);
    
    ws.onopen = () => {
      console.log('✓ Connected to Chrome Automation API server');
      if (reconnectInterval) {
        clearInterval(reconnectInterval);
        reconnectInterval = null;
      }
      startHeartbeat();
    };
    
    ws.onmessage = async (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === 'pong') return;
        
        const response = await handleCommand(message);
        ws.send(JSON.stringify(response));
      } catch (error) {
        console.error('Error handling message:', error);
        const message = JSON.parse(event.data);
        ws.send(JSON.stringify({
          success: false,
          error: error.message,
          requestId: message?.requestId
        }));
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
      console.log('✗ Disconnected from server, reconnecting...');
      ws = null;
      stopHeartbeat();
      
      if (!reconnectInterval) {
        reconnectInterval = setInterval(() => {
          console.log('Attempting to reconnect...');
          connectWebSocket();
        }, RECONNECT_DELAY);
      }
    };
  } catch (error) {
    console.error('Failed to connect:', error);
  }
}

function startHeartbeat() {
  if (heartbeatInterval) clearInterval(heartbeatInterval);
  
  heartbeatInterval = setInterval(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'ping' }));
    }
  }, HEARTBEAT_INTERVAL);
}

function stopHeartbeat() {
  if (heartbeatInterval) {
    clearInterval(heartbeatInterval);
    heartbeatInterval = null;
  }
}

// Keep service worker alive
function startKeepAlive() {
  if (keepAliveInterval) clearInterval(keepAliveInterval);
  
  keepAliveInterval = setInterval(() => {
    chrome.runtime.getPlatformInfo(() => {});
  }, KEEP_ALIVE_INTERVAL);
}

// Command Handler
async function handleCommand(message) {
  const { action, requestId } = message;
  
  try {
    let result;
    
    switch (action) {
      case 'createTab':
        result = await createTab(message.url, message.active);
        break;
      case 'getTabs':
        result = await getTabs(message.filter);
        break;
      case 'getActiveTab':
        result = await getActiveTab();
        break;
      case 'navigateTab':
        result = await navigateTab(message.tabId, message.url);
        break;
      case 'activateTab':
        result = await activateTab(message.tabId);
        break;
      case 'closeTab':
        result = await closeTab(message.tabId);
        break;
      case 'reloadTab':
        result = await reloadTab(message.tabId, message.bypassCache);
        break;
      case 'getContent':
        result = await getContent(message.tabId, message.format);
        break;
      case 'getMetadata':
        result = await getMetadata(message.tabId);
        break;
      case 'interact':
        result = await interact(message.tabId, message.interaction);
        break;
      default:
        throw new Error(`Unknown action: ${action}`);
    }
    
    return { ...result, requestId };
  } catch (error) {
    return { 
      success: false, 
      error: error.message,
      requestId 
    };
  }
}

// Tab Operations
async function createTab(url, active = true) {
  const tab = await chrome.tabs.create({ url, active });
  await waitForTabLoad(tab.id);
  
  return {
    success: true,
    tab: {
      id: tab.id,
      url: tab.url,
      title: tab.title,
      active: tab.active,
      windowId: tab.windowId
    }
  };
}

async function getTabs(filter = {}) {
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
      status: tab.status
    }))
  };
}

async function getActiveTab() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tabs.length === 0) throw new Error('No active tab found');
  
  return {
    success: true,
    tab: {
      id: tabs[0].id,
      url: tabs[0].url,
      title: tabs[0].title,
      active: tabs[0].active
    }
  };
}

async function navigateTab(tabId, url) {
  await chrome.tabs.update(tabId, { url });
  await waitForTabLoad(tabId);
  const tab = await chrome.tabs.get(tabId);
  
  return {
    success: true,
    tab: {
      id: tab.id,
      url: tab.url,
      title: tab.title
    }
  };
}

async function activateTab(tabId) {
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
}

async function closeTab(tabId) {
  await chrome.tabs.remove(tabId);
  return { success: true };
}

async function reloadTab(tabId, bypassCache = false) {
  await chrome.tabs.reload(tabId, { bypassCache });
  await waitForTabLoad(tabId);
  return { success: true };
}

async function waitForTabLoad(tabId, timeout = 30000) {
  return new Promise((resolve) => {
    const listener = (updatedTabId, info) => {
      if (updatedTabId === tabId && info.status === 'complete') {
        chrome.tabs.onUpdated.removeListener(listener);
        resolve();
      }
    };
    chrome.tabs.onUpdated.addListener(listener);
    setTimeout(() => {
      chrome.tabs.onUpdated.removeListener(listener);
      resolve();
    }, timeout);
  });
}

// Content Extraction
async function getContent(tabId, format = 'html') {
  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: extractPageContent,
    args: [format]
  });
  
  return {
    success: true,
    content: results[0].result
  };
}

async function getMetadata(tabId) {
  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: extractMetadata
  });
  
  return {
    success: true,
    metadata: results[0].result
  };
}

// Injected Functions
// Always extract HTML - Python will handle markdown conversion
function extractPageContent() {
  return {
    url: window.location.href,
    title: document.title,
    timestamp: new Date().toISOString(),
    html: document.documentElement.outerHTML,
    bodyHtml: document.body.innerHTML,
    text: document.body.innerText,
    format: 'html'
  };
}

function extractMetadata() {
  const metadata = {
    url: window.location.href,
    title: document.title,
    description: '',
    keywords: [],
    author: '',
    timestamp: new Date().toISOString()
  };
  
  document.querySelectorAll('meta').forEach(tag => {
    const name = tag.getAttribute('name') || tag.getAttribute('property');
    const content = tag.getAttribute('content');
    
    if (name && content) {
      if (name.includes('description')) metadata.description = content;
      else if (name.includes('keywords')) metadata.keywords = content.split(',').map(k => k.trim());
      else if (name.includes('author')) metadata.author = content;
      else if (name === 'og:title') metadata.ogTitle = content;
      else if (name === 'og:description') metadata.ogDescription = content;
    }
  });
  
  return metadata;
}

// Page Interactions
async function interact(tabId, interaction) {
  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: performInteraction,
    args: [interaction]
  });
  
  return {
    success: true,
    result: results[0].result
  };
}

function performInteraction(interaction) {
  const { action, selector, value, timeout } = interaction;
  
  return new Promise((resolve, reject) => {
    try {
      switch (action) {
        case 'click':
          const clickEl = document.querySelector(selector);
          if (!clickEl) throw new Error(`Element not found: ${selector}`);
          
          // Scroll element into view before clicking
          clickEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
          
          // Wait a moment for scroll, then click
          setTimeout(() => {
            clickEl.click();
            resolve({ 
              success: true, 
              action: 'click', 
              selector,
              elementTag: clickEl.tagName,
              elementText: clickEl.innerText?.substring(0, 50) || ''
            });
          }, 300);
          break;
          
        case 'input':
          const inputEl = document.querySelector(selector);
          if (!inputEl) throw new Error(`Element not found: ${selector}`);
          
          // Focus the element first
          inputEl.focus();
          
          // Clear existing value
          inputEl.value = '';
          
          // Set new value
          inputEl.value = value;
          
          // Trigger events that frameworks listen to
          inputEl.dispatchEvent(new Event('input', { bubbles: true }));
          inputEl.dispatchEvent(new Event('change', { bubbles: true }));
          inputEl.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true }));
          inputEl.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
          
          resolve({ 
            success: true, 
            action: 'input', 
            selector, 
            value,
            elementTag: inputEl.tagName,
            elementType: inputEl.type || 'text'
          });
          break;
          
        case 'select':
          const select = document.querySelector(selector);
          if (!select) throw new Error(`Element not found: ${selector}`);
          select.value = value;
          select.dispatchEvent(new Event('change', { bubbles: true }));
          resolve({ success: true, action: 'select', selector, value });
          break;
          
        case 'wait':
          setTimeout(() => resolve({ success: true, action: 'wait', duration: timeout }), timeout || 1000);
          break;
          
        case 'waitForElement':
          let elapsed = 0;
          const check = () => {
            if (document.querySelector(selector)) {
              resolve({ success: true, action: 'waitForElement', selector });
            } else if (elapsed >= (timeout || 5000)) {
              reject(new Error(`Timeout waiting for: ${selector}`));
            } else {
              elapsed += 100;
              setTimeout(check, 100);
            }
          };
          check();
          break;
          
        case 'getText':
          const textEl = document.querySelector(selector);
          if (!textEl) throw new Error(`Element not found: ${selector}`);
          resolve({ success: true, action: 'getText', selector, text: textEl.innerText });
          break;
          
        case 'getAttribute':
          const attrEl = document.querySelector(selector);
          if (!attrEl) throw new Error(`Element not found: ${selector}`);
          const attrValue = attrEl.getAttribute(value);
          resolve({ 
            success: true, 
            action: 'getAttribute', 
            selector,
            attribute: value,
            value: attrValue 
          });
          break;
        
        case 'findElement':
          // Find element and return its details
          const foundEl = document.querySelector(selector);
          if (!foundEl) {
            resolve({ 
              success: false, 
              action: 'findElement', 
              selector,
              found: false
            });
          } else {
            const rect = foundEl.getBoundingClientRect();
            resolve({ 
              success: true, 
              action: 'findElement', 
              selector,
              found: true,
              element: {
                tag: foundEl.tagName,
                id: foundEl.id,
                className: foundEl.className,
                text: foundEl.innerText?.substring(0, 100) || '',
                visible: rect.width > 0 && rect.height > 0,
                position: {
                  x: rect.x,
                  y: rect.y,
                  width: rect.width,
                  height: rect.height
                }
              }
            });
          }
          break;
          
        default:
          reject(new Error(`Unknown action: ${action}`));
      }
    } catch (error) {
      reject(error);
    }
  });
}

// Initialize
chrome.runtime.onInstalled.addListener(() => {
  console.log('Chrome Automation API extension installed');
  startKeepAlive();
  connectWebSocket();
});

chrome.runtime.onStartup.addListener(() => {
  console.log('Chrome Automation API extension started');
  startKeepAlive();
  connectWebSocket();
});

startKeepAlive();
connectWebSocket();

console.log('Chrome Automation API - Background script loaded (all-in-one)');
