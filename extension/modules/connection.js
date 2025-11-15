/**
 * WebSocket Connection Module
 * Handles connection, reconnection, and heartbeat
 */

export class ConnectionManager {
  constructor(config) {
    this.wsUrl = config.wsUrl;
    this.reconnectDelay = config.reconnectDelay || 5000;
    this.heartbeatInterval = config.heartbeatInterval || 30000;
    
    this.ws = null;
    this.reconnectInterval = null;
    this.heartbeatTimer = null;
    this.messageHandler = null;
  }
  
  connect() {
    try {
      this.ws = new WebSocket(this.wsUrl);
      
      this.ws.onopen = () => this.handleOpen();
      this.ws.onmessage = (event) => this.handleMessage(event);
      this.ws.onerror = (error) => this.handleError(error);
      this.ws.onclose = () => this.handleClose();
      
    } catch (error) {
      console.error('Failed to connect:', error);
    }
  }
  
  handleOpen() {
    console.log('✓ Connected to Chrome Automation API server');
    
    // Clear reconnect interval
    if (this.reconnectInterval) {
      clearInterval(this.reconnectInterval);
      this.reconnectInterval = null;
    }
    
    // Start heartbeat
    this.startHeartbeat();
  }
  
  async handleMessage(event) {
    try {
      const message = JSON.parse(event.data);
      
      // Ignore pong responses
      if (message.type === 'pong') {
        return;
      }
      
      // Call message handler
      if (this.messageHandler) {
        const response = await this.messageHandler(message);
        this.send(response);
      }
      
    } catch (error) {
      console.error('Error handling message:', error);
      const message = JSON.parse(event.data);
      this.send({
        success: false,
        error: error.message,
        requestId: message?.requestId
      });
    }
  }
  
  handleError(error) {
    console.error('WebSocket error:', error);
  }
  
  handleClose() {
    console.log('✗ Disconnected from server, reconnecting...');
    this.ws = null;
    
    // Clear heartbeat
    this.stopHeartbeat();
    
    // Start reconnection
    if (!this.reconnectInterval) {
      this.reconnectInterval = setInterval(() => {
        console.log('Attempting to reconnect...');
        this.connect();
      }, this.reconnectDelay);
    }
  }
  
  startHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
    }
    
    this.heartbeatTimer = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.send({ type: 'ping' });
      }
    }, this.heartbeatInterval);
  }
  
  stopHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }
  
  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
  
  setMessageHandler(handler) {
    this.messageHandler = handler;
  }
  
  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
}
