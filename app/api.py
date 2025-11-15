"""FastAPI application and routes"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import tabs, websocket
from app import __version__

app = FastAPI(
    title="Chrome Automation API",
    version=__version__,
    description="Production-ready browser automation via REST API"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(websocket.router)
app.include_router(tabs.router, prefix="/tab", tags=["tabs"])

@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    from app.services.extension import extension_service
    
    return {
        "name": "Chrome Automation API",
        "version": __version__,
        "status": "running",
        "extension_connected": extension_service.is_connected()
    }

@app.get("/health", tags=["health"])
async def health():
    """Detailed health check"""
    from app.services.extension import extension_service
    
    return {
        "status": "healthy",
        "extension": {
            "connected": extension_service.is_connected(),
            "pending_requests": len(extension_service.pending_requests)
        }
    }
