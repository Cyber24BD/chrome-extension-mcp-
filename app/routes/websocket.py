"""WebSocket route for extension communication"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.extension import extension_service

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for Chrome extension connection"""
    
    await extension_service.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle ping/pong for keepalive
            if data.get('type') == 'ping':
                await websocket.send_json({'type': 'pong'})
                continue
            
            await extension_service.handle_message(data)
            
    except WebSocketDisconnect:
        extension_service.disconnect()
    except Exception as e:
        print(f"WebSocket error: {e}")
        extension_service.disconnect()
