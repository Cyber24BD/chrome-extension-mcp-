"""Extension communication service"""

import asyncio
import uuid
from typing import Dict, Any, Optional
from fastapi import WebSocket, HTTPException
from app.config import settings

class ExtensionService:
    """Manages communication with Chrome extension"""
    
    def __init__(self):
        self.websocket: Optional[WebSocket] = None
        self.pending_requests: Dict[str, asyncio.Future] = {}
    
    def is_connected(self) -> bool:
        """Check if extension is connected"""
        return self.websocket is not None
    
    async def connect(self, websocket: WebSocket):
        """Connect extension via WebSocket"""
        await websocket.accept()
        self.websocket = websocket
        print("✓ Chrome extension connected")
    
    def disconnect(self):
        """Disconnect extension"""
        self.websocket = None
        print("✗ Chrome extension disconnected")
        
        # Cancel all pending requests
        for future in self.pending_requests.values():
            if not future.done():
                future.cancel()
        self.pending_requests.clear()
    
    async def handle_message(self, data: Dict[str, Any]):
        """Handle incoming message from extension"""
        request_id = data.get('requestId')
        
        if request_id and request_id in self.pending_requests:
            future = self.pending_requests[request_id]
            if not future.done():
                future.set_result(data)
    
    async def send_command(
        self, 
        command: Dict[str, Any], 
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """Send command to extension and wait for response"""
        
        if not self.is_connected():
            raise HTTPException(
                status_code=503, 
                detail="Chrome extension not connected. Please ensure the extension is installed and running."
            )
        
        request_id = str(uuid.uuid4())
        command['requestId'] = request_id
        
        # Create future for response
        future = asyncio.Future()
        self.pending_requests[request_id] = future
        
        try:
            # Send command
            await self.websocket.send_json(command)
            
            # Wait for response
            timeout_value = timeout or settings.EXTENSION_RESPONSE_TIMEOUT
            response = await asyncio.wait_for(future, timeout=timeout_value)
            
            # Check for errors in response
            if not response.get('success', False):
                error_msg = response.get('error', 'Unknown error from extension')
                raise HTTPException(status_code=500, detail=error_msg)
            
            return response
            
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504, 
                detail=f"Extension did not respond within {timeout_value} seconds"
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            self.pending_requests.pop(request_id, None)

# Global instance
extension_service = ExtensionService()
