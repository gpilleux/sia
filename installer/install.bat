@echo off
REM SIA Installer Script for Windows
REM Usage: install.bat

echo.
echo ========================================
echo  SIA Framework Installer (Windows)
echo ========================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check for uv
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] 'uv' is not installed. Installing...
    pip install uv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install uv
        pause
        exit /b 1
    )
)

echo.
echo [STEP 1/2] Running Auto-Discovery...
echo ---------------------------------------------------
uv run sia\installer\auto_discovery.py
if %errorlevel% neq 0 (
    echo [ERROR] Auto-discovery failed
    pause
    exit /b 1
)

echo.
echo ---------------------------------------------------
echo [SUCCESS] SIA Installation Complete!
echo.
echo   Created:
echo   - Configuration: .sia.detected.yaml
echo   - Instructions: .github\copilot-instructions.md
echo.
echo Next steps:
echo   1. Review .sia.detected.yaml
echo   2. Read .github\copilot-instructions.md
echo   3. Start using GitHub Copilot with SIA!
echo.
pause
