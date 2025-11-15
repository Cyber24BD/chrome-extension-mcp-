@echo off
echo ========================================
echo Installing MCP Server Dependencies
echo ========================================
echo.

pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure API server is running: python main.py
echo 2. Add to Claude Desktop config (see README.md)
echo 3. Restart Claude Desktop
echo.
pause
