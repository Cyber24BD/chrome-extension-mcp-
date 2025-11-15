"""
API Client for Browser Automation Server
"""

from typing import Any, Optional
import httpx
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import API_BASE_URL, API_TIMEOUT


class APIClient:
    """HTTP client for browser automation API"""
    
    def __init__(self, base_url: str = API_BASE_URL, timeout: float = API_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    async def get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout
            )
        return self._client
    
    async def close(self):
        """Close HTTP client"""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def call(self, method: str, endpoint: str, **kwargs) -> dict[str, Any]:
        """Make API call to browser automation server"""
        client = await self.get_client()
        
        try:
            if method.upper() == "GET":
                response = await client.get(endpoint, **kwargs)
            elif method.upper() == "POST":
                response = await client.post(endpoint, **kwargs)
            elif method.upper() == "DELETE":
                response = await client.delete(endpoint, **kwargs)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"success": False, "error": str(e)}


# Global client instance
_global_client: Optional[APIClient] = None


def get_client() -> APIClient:
    """Get global API client instance"""
    global _global_client
    if _global_client is None:
        _global_client = APIClient()
    return _global_client


async def call_api(method: str, endpoint: str, **kwargs) -> dict[str, Any]:
    """Convenience function to call API"""
    client = get_client()
    return await client.call(method, endpoint, **kwargs)
