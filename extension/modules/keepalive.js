/**
 * Keep-Alive Module
 * Prevents service worker from sleeping
 */

export class KeepAliveManager {
  constructor(interval = 20000) {
    this.interval = interval;
    this.timer = null;
  }
  
  start() {
    if (this.timer) {
      this.stop();
    }
    
    this.timer = setInterval(() => {
      // Ping to keep service worker alive
      chrome.runtime.getPlatformInfo(() => {
        // This keeps the service worker active
      });
    }, this.interval);
    
    console.log('Keep-alive started');
  }
  
  stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }
}
