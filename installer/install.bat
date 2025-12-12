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
echo [STEP 1/4] Creating .sia\ Directory Structure...
echo ---------------------------------------------------
mkdir .sia\agents 2>nul
mkdir .sia\knowledge\active 2>nul
mkdir .sia\knowledge\_archive 2>nul
mkdir .sia\requirements 2>nul
mkdir .sia\requirements\_archive 2>nul
mkdir .sia\skills 2>nul
mkdir .sia\prompts 2>nul
mkdir .vscode 2>nul

REM Create README files
(
echo # SIA Project Configuration
echo.
echo This directory contains the SIA framework integration for this project.
echo.
echo ## Structure
echo - `agents/`: Project-specific agent definitions
echo - `knowledge/`: Active and archived knowledge base
echo - `requirements/`: Requirements management ^(active and archived^)
echo - `skills/`: Project-specific automation skills
echo.
echo See `sia/README.md` for complete framework documentation.
) > .sia\README.md

(
echo # Project Agents
echo.
echo Define project-specific agents here. The SUPER AGENT will populate this
echo directory during repository initialization.
echo.
echo ## Next Steps
echo Ask GitHub Copilot: "Initialize SIA agents for this repository"
) > .sia\agents\README.md

(
echo # Active Knowledge Base
echo.
echo Active research, decisions, and domain knowledge.
echo.
echo ## Document Lifecycle
echo See `.github/DOCUMENT_LIFECYCLE.md` for archival protocol.
) > .sia\knowledge\active\README.md

(
echo # Requirements Management
echo.
echo See `sia/requirements/README.md` for complete workflow.
echo.
echo ## Quick Start
echo 1. Define requirements in natural language
echo 2. SUPER AGENT decomposes into QUANT tasks
echo 3. Execute, verify, archive
) > .sia\requirements\README.md

(
echo # Project Skills
echo.
echo Project-specific automation scripts.
echo.
echo ## Framework Skills
echo Reusable skills available in `sia/skills/`
) > .sia\skills\README.md

REM Copy INIT_REQUIRED template
copy sia\templates\INIT_REQUIRED.template.md .sia\INIT_REQUIRED.md >nul

REM Copy slash commands (prompts)
echo    [INFO] Installing slash commands...
xcopy sia\templates\prompts\*.prompt.md .sia\prompts\ /Y /Q >nul

REM Install file reader skills
echo    [INFO] Installing file reader skills...
if exist sia\templates\skills\file_readers (
    mkdir .sia\skills\file_readers 2>nul
    xcopy sia\templates\skills\file_readers\* .sia\skills\file_readers\ /E /Y /Q >nul
    copy sia\templates\skills\read_*.py .sia\skills\ >nul 2>&1
    echo    [OK] File readers installed (DOCX, XLSX, PDF)
) else (
    echo    [WARN] File readers not found in templates (framework might be outdated)
)

REM Install VS Code settings
if exist .vscode\settings.json (
    echo    [WARN] .vscode\settings.json already exists, skipping...
    echo           Review sia\templates\vscode-settings.template.json for recommended settings
) else (
    echo    [INFO] Creating .vscode\settings.json...
    REM Simple placeholder replacement for Windows
    powershell -Command "(Get-Content sia\templates\vscode-settings.template.json) -replace '{{LOCALE}}', 'en' -replace '{{EXTRA_PATHS}}', '' | Set-Content .vscode\settings.json"
)

REM Install .gitignore if not exists
if exist .gitignore (
    echo    [WARN] .gitignore already exists, skipping...
    echo           Review sia\templates\gitignore.template for recommended exclusions
) else (
    echo    [INFO] Creating .gitignore from template...
    copy sia\templates\gitignore.template .gitignore >nul
)

echo    [OK] .sia\ structure created
echo    [OK] .sia\prompts\ slash commands installed
echo    [OK] .vscode\settings.json configured
echo    [OK] .sia\INIT_REQUIRED.md created (one-time init instructions)

echo.
echo [STEP 2/4] Running Smart Initialization...
echo ---------------------------------------------------
uv run --with pyyaml python sia\installer\smart_init.py
if %errorlevel% neq 0 (
    echo [ERROR] Smart initialization failed
    pause
    exit /b 1
)

echo.
echo ---------------------------------------------------
echo [STEP 3/4] Installing Copilot Instructions...
echo ---------------------------------------------------
mkdir .github 2>nul
if exist .github\copilot-instructions.md (
    echo    [WARN] .github\copilot-instructions.md already exists, skipping...
    echo           Review sia\core\copilot-instructions.template.md for updates
) else (
    echo    [INFO] Creating .github\copilot-instructions.md from template...
    copy sia\core\copilot-instructions.template.md .github\copilot-instructions.md >nul
    echo    [WARN] Manual customization required:
    echo           Edit .github\copilot-instructions.md and replace placeholders:
    echo           - {{PROJECT_NAME}}
    echo           - {{PROJECT_TYPE}}
    echo           - {{PROJECT_MISSION}}
    echo           - {{TECH_STACK}}
    echo           - {{ARCHITECTURE_PATTERN}}
    echo           - {{EXECUTION_COMMAND}}
    echo           - {{ARCHITECTURE_DNA}}
    echo           - {{RESEARCH_SOURCES}}
    echo           - {{PROJECT_SLUG}}
    echo           - {{ADDITIONAL_CONTEXT}}
)

echo.
echo ---------------------------------------------------
echo [STEP 4/4] Repository Initialization Required
echo ---------------------------------------------------
echo.
echo [SUCCESS] SIA Installation Complete!
echo.
echo   Created:
echo   - Directory: .sia\ (agents, knowledge, requirements, skills, prompts)
echo   - Directory: .vscode\ (VS Code configuration)
echo   - Configuration: .sia.detected.yaml
echo   - Configuration: .vscode\settings.json (slash commands enabled)
echo   - Instructions: .github\copilot-instructions.md
echo   - Init Protocol: .sia\INIT_REQUIRED.md (one-time)
echo   - Slash Commands: .sia\prompts\*.prompt.md (11 commands)
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
echo      - Detect specialized agents (e.g., Repository Guardian)
echo      - Create initial knowledge base
echo      - Populate skills catalog
echo      - Delete .sia\INIT_REQUIRED.md (auto-cleanup)
echo.
echo   3. Review generated files in .sia\
echo   4. Start working with natural language requirements!
echo.
echo Documentation:
echo   - Framework: sia\README.md
echo   - Quick Start: sia\QUICKSTART.md
echo   - Distribution: sia\DISTRIBUTION.md
echo.
pause
