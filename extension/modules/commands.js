/**
 * Command Handler Module
 * Routes commands to appropriate modules
 */

import { TabManager } from './tabs.js';
import { ContentExtractor } from './content.js';
import { InteractionManager } from './interactions.js';

export class CommandHandler {
  constructor() {
    this.tabManager = new TabManager();
    this.contentExtractor = new ContentExtractor();
    this.interactionManager = new InteractionManager();
  }
  
  async handle(message) {
    const { action, requestId } = message;
    
    try {
      let result;
      
      switch (action) {
        case 'createTab':
          result = await this.tabManager.createTab(message.url, message.active);
          break;
          
        case 'getTabs':
          result = await this.tabManager.getTabs(message.filter);
          break;
          
        case 'getActiveTab':
          result = await this.tabManager.getActiveTab();
          break;
          
        case 'navigateTab':
          result = await this.tabManager.navigateTab(message.tabId, message.url);
          break;
          
        case 'activateTab':
          result = await this.tabManager.activateTab(message.tabId);
          break;
          
        case 'closeTab':
          result = await this.tabManager.closeTab(message.tabId);
          break;
          
        case 'reloadTab':
          result = await this.tabManager.reloadTab(message.tabId, message.bypassCache);
          break;
          
        case 'getContent':
          result = await this.contentExtractor.getContent(
            message.tabId, 
            message.format || 'html'
          );
          break;
          
        case 'getMetadata':
          result = await this.contentExtractor.getPageMetadata(message.tabId);
          break;
          
        case 'interact':
          result = await this.interactionManager.interact(
            message.tabId, 
            message.interaction
          );
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
}
