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
echo [STEP 1/3] Creating .sia\ Directory Structure...
echo ---------------------------------------------------
mkdir .sia\agents 2>nul
mkdir .sia\knowledge\active 2>nul
mkdir .sia\knowledge\_archive 2>nul
mkdir .sia\requirements 2>nul
mkdir .sia\requirements\_archive 2>nul
mkdir .sia\skills 2>nul

REM Create README files
echo # SIA Project Configuration > .sia\README.md
echo. >> .sia\README.md
echo This directory contains the SIA framework integration for this project. >> .sia\README.md
echo See sia\README.md for complete framework documentation. >> .sia\README.md

echo # Project Agents > .sia\agents\README.md
echo. >> .sia\agents\README.md
echo Ask GitHub Copilot: "Initialize SIA agents for this repository" >> .sia\agents\README.md

echo # Active Knowledge Base > .sia\knowledge\active\README.md
echo See .github\DOCUMENT_LIFECYCLE.md for archival protocol. >> .sia\knowledge\active\README.md

echo # Requirements Management > .sia\requirements\README.md
echo See sia\requirements\README.md for complete workflow. >> .sia\requirements\README.md

echo # Project Skills > .sia\skills\README.md
echo Reusable skills available in sia\skills\ >> .sia\skills\README.md

REM Copy INIT_REQUIRED template
copy sia\templates\INIT_REQUIRED.template.md .sia\INIT_REQUIRED.md >nul

echo    [OK] .sia\ structure created
echo    [OK] .sia\INIT_REQUIRED.md created (one-time init instructions)

echo.
echo [STEP 2/3] Running Auto-Discovery...
echo ---------------------------------------------------
uv run sia\installer\auto_discovery.py
if %errorlevel% neq 0 (
    echo [ERROR] Auto-discovery failed
    pause
    exit /b 1
)

echo.
echo ---------------------------------------------------
echo [STEP 3/3] Repository Initialization Required
echo ---------------------------------------------------
echo.
echo [SUCCESS] SIA Installation Complete!
echo.
echo   Created:
echo   - Directory: .sia\ (agents, knowledge, requirements, skills)
echo   - Configuration: .sia.detected.yaml
echo   - Instructions: .github\copilot-instructions.md
echo   - Init Protocol: .sia\INIT_REQUIRED.md (one-time)
echo.
echo   WARNING: Repository requires SUPER AGENT initialization
echo.
echo Next steps:
echo   1. Open this project in VS Code with GitHub Copilot
echo   2. Ask Copilot: 'Initialize SIA for this repository'
echo.
echo      The SUPER AGENT will:
echo      - Analyze repository structure and domain
echo      - Generate project SPR (.sia\agents\^<project^>.md)
echo      - Detect specialized agents
echo      - Create initial knowledge base
echo      - Populate skills catalog
echo.
echo   3. Review generated files in .sia\
echo   4. Start working with natural language requirements!
echo.
echo Documentation:
echo   - Framework: sia\README.md
echo   - Quick Start: sia\QUICKSTART.md
echo   - Uninstall: sia\UNINSTALL.md
echo.
pause
