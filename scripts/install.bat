@echo off
echo Installing Chrome Automation API dependencies...
echo.
uv pip install -r requirements.txt
echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Load extension in Chrome (chrome://extensions/)
echo 2. Run: start.bat
pause
