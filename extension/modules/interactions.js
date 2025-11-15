/**
 * Page Interaction Module
 * Handles DOM interactions
 */

export class InteractionManager {
  
  async interact(tabId, interaction) {
    try {
      const results = await chrome.scripting.executeScript({
        target: { tabId },
        func: this.performInteraction,
        args: [interaction]
      });
      
      const result = results && results[0] ? results[0].result : null;
      
      return {
        success: true,
        result: result,
        tabId: tabId
      };
    } catch (error) {
      throw new Error(`Failed to interact: ${error.message}`);
    }
  }
  
  // Injected function - runs in page context
  performInteraction(interaction) {
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
            const selectEl = document.querySelector(selector);
            if (!selectEl) throw new Error(`Element not found: ${selector}`);
            selectEl.value = value;
            selectEl.dispatchEvent(new Event('change', { bubbles: true }));
            resolve({ success: true, action: 'select', selector, value });
            break;
            
          case 'wait':
            setTimeout(() => {
              resolve({ success: true, action: 'wait', duration: timeout });
            }, timeout || 1000);
            break;
            
          case 'waitForElement':
            let elapsed = 0;
            const checkInterval = 100;
            const maxTimeout = timeout || 5000;
            
            const checkElement = () => {
              if (document.querySelector(selector)) {
                resolve({ success: true, action: 'waitForElement', selector });
              } else if (elapsed >= maxTimeout) {
                reject(new Error(`Timeout waiting for element: ${selector}`));
              } else {
                elapsed += checkInterval;
                setTimeout(checkElement, checkInterval);
              }
            };
            checkElement();
            break;
            
          case 'getText':
            const textEl = document.querySelector(selector);
            if (!textEl) throw new Error(`Element not found: ${selector}`);
            resolve({ 
              success: true, 
              action: 'getText', 
              selector,
              text: textEl.innerText 
            });
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
            reject(new Error(`Unknown interaction action: ${action}`));
        }
      } catch (error) {
        reject(error);
      }
    });
  }
}
