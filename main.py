#!/usr/bin/env python3
"""
Chrome Automation API - Main Entry Point
Production-ready browser automation via REST API
"""

import sys
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Chrome Automation API Server")
    print("="*70)
    print(f"\n✓ Server: http://{settings.HOST}:{settings.PORT}")
    print(f"✓ API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"✓ WebSocket: ws://{settings.HOST}:{settings.PORT}/ws")
    print("\nWaiting for Chrome extension to connect...\n")
    
    try:
        uvicorn.run(
            "app.api:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level=settings.LOG_LEVEL.lower()
        )
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
        sys.exit(0)
