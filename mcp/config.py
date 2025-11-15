"""
Configuration for MCP Server
"""

import os
from typing import Optional

# API Configuration
API_BASE_URL = os.getenv("BROWSER_API_URL", "http://localhost:8000")
API_TIMEOUT = float(os.getenv("BROWSER_API_TIMEOUT", "30.0"))

# Server Configuration
SERVER_NAME = "browser-automation"
SERVER_VERSION = "1.0.0"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
