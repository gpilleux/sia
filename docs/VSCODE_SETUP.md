# VS Code Setup Guide

**SIA Framework** - Optimal IDE configuration for Super Agent workflows

---

## Table of Contents

1. [Quick Setup](#quick-setup)
2. [Required Extensions](#required-extensions)
3. [Recommended Extensions](#recommended-extensions)
4. [Settings Configuration](#settings-configuration)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Troubleshooting](#troubleshooting)

---

## Quick Setup

The SIA installer (`sia/installer/install.sh`) automatically creates `.vscode/settings.json` with:

- ✅ Slash commands enabled (`.sia/prompts`)
- ✅ GitHub Copilot configured
- ✅ Python analysis settings
- ✅ Formatting on save
- ✅ File exclusions

**Manual setup:** Copy `sia/templates/vscode-settings.template.json` → `.vscode/settings.json`

---

## Required Extensions

### 1. GitHub Copilot
**ID:** `GitHub.copilot`

Essential for Super Agent interaction. Provides:
- Inline code suggestions
- Chat interface for slash commands
- Context-aware completions

**Install:**
```bash
code --install-extension GitHub.copilot
```

### 2. Python
**ID:** `ms-python.python`

Core Python support:
- IntelliSense
- Linting
- Debugging
- Test discovery

**Install:**
```bash
code --install-extension ms-python.python
```

### 3. Pylance
**ID:** `ms-python.vscode-pylance`

Fast, feature-rich language server:
- Type checking
- Auto-imports
- Code navigation
- Refactoring

**Install:**
```bash
code --install-extension ms-python.vscode-pylance
```

### 4. Black Formatter
**ID:** `ms-python.black-formatter`

Code formatting:
- Automatic formatting on save
- Consistent code style
- 88-character line length

**Install:**
```bash
code --install-extension ms-python.black-formatter
```

---

## Recommended Extensions

### Development

**Flake8**
- **ID:** `ms-python.flake8`
- **Purpose:** Linting for style guide enforcement

**isort**
- **ID:** `ms-python.isort`
- **Purpose:** Import sorting

**Better Comments**
- **ID:** `aaron-bond.better-comments`
- **Purpose:** Color-coded comments (TODO, FIXME, etc.)

**Error Lens**
- **ID:** `usernamehw.errorlens`
- **Purpose:** Inline error highlighting

### Testing

**Python Test Explorer**
- **ID:** `LittleFoxTeam.vscode-python-test-adapter`
- **Purpose:** Visual test runner

**Coverage Gutters**
- **ID:** `ryanluker.vscode-coverage-gutters`
- **Purpose:** Coverage visualization

### Docker (if applicable)

**Docker**
- **ID:** `ms-azuretools.vscode-docker`
- **Purpose:** Dockerfile support, container management

### Git

**GitLens**
- **ID:** `eamodio.gitlens`
- **Purpose:** Enhanced Git integration

**Git Graph**
- **ID:** `mhutchie.git-graph`
- **Purpose:** Visual Git history

### Productivity

**Markdown All in One**
- **ID:** `yzhang.markdown-all-in-one`
- **Purpose:** Markdown editing (for `.sia/` docs)

**Code Spell Checker**
- **ID:** `streetsidesoftware.code-spell-checker`
- **Purpose:** Spelling errors in code/comments

---

## Settings Configuration

### Core Settings (via template)

```json
{
    "// GitHub Copilot": "",
    "github.copilot.chat.codeGeneration.useInstructionFiles": true,
    "github.copilot.chat.scopeSelection": true,
    "github.copilot.chat.localeOverride": "en",
    
    "// SIA Slash Commands": "",
    "chat.promptFilesLocations": {
        ".sia/prompts": true
    },
    
    "// Python": "",
    "python.analysis.extraPaths": ["${workspaceFolder}"],
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    
    "// Editor": "",
    "editor.rulers": [88, 120],
    "editor.formatOnSave": true,
    
    "// Formatting": "",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    
    "// File Exclusions": "",
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/htmlcov": true,
        "**/.coverage": true
    }
}
```

### Custom Settings Per Project

**Python Paths:**
```json
"python.analysis.extraPaths": [
    "${workspaceFolder}/backend/src",
    "${workspaceFolder}/domain",
    "${workspaceFolder}/infrastructure"
]
```

**Locale:**
```json
"github.copilot.chat.localeOverride": "es"  // Spanish
"github.copilot.chat.localeOverride": "en"  // English
```

**Additional Exclusions:**
```json
"files.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.venv": true
}
```

---

## Keyboard Shortcuts

### Super Agent Workflow

| Action | Shortcut (macOS) | Shortcut (Windows/Linux) |
|--------|------------------|--------------------------|
| Open Copilot Chat | `⌘ I` | `Ctrl+I` |
| Inline Suggest | `Tab` | `Tab` |
| Dismiss Suggest | `Esc` | `Esc` |
| Quick Fix | `⌘ .` | `Ctrl+.` |

### Code Navigation

| Action | Shortcut (macOS) | Shortcut (Windows/Linux) |
|--------|------------------|--------------------------|
| Go to Definition | `F12` | `F12` |
| Peek Definition | `⌥ F12` | `Alt+F12` |
| Go to Symbol | `⌘ T` | `Ctrl+T` |
| Find References | `⇧ F12` | `Shift+F12` |

### Testing

| Action | Shortcut (macOS) | Shortcut (Windows/Linux) |
|--------|------------------|--------------------------|
| Run Tests | `⌘ ; T` | `Ctrl+; T` |
| Debug Test | `⌘ ; D` | `Ctrl+; D` |

### Custom Shortcuts (Recommended)

Add to `keybindings.json`:

```json
[
    {
        "key": "cmd+shift+a",
        "command": "workbench.action.chat.open",
        "args": "/activate"
    },
    {
        "key": "cmd+shift+t",
        "command": "workbench.action.chat.open",
        "args": "/test"
    }
]
```

---

## Troubleshooting

### Slash Commands Not Appearing

**Problem:** Prompts in `.sia/prompts/` not showing in Copilot Chat

**Solution:**
1. Verify `.vscode/settings.json` contains:
   ```json
   "chat.promptFilesLocations": {
       ".sia/prompts": true
   }
   ```
2. Reload VS Code window: `⌘ Shift P` → "Reload Window"
3. Check prompt files have `.prompt.md` extension
4. Verify frontmatter format:
   ```markdown
   ---
   name: commandname
   description: Description
   ---
   ```

### Copilot Not Reading Instructions

**Problem:** Copilot ignoring `.github/copilot-instructions.md`

**Solution:**
1. Verify setting:
   ```json
   "github.copilot.chat.codeGeneration.useInstructionFiles": true
   ```
2. Ensure file is exactly at `.github/copilot-instructions.md`
3. Reload window
4. Explicitly reference in chat: "Read .github/copilot-instructions.md"

### Python Analysis Issues

**Problem:** Import errors, IntelliSense not working

**Solution:**
1. Select Python interpreter: `⌘ Shift P` → "Python: Select Interpreter"
2. Verify `python.analysis.extraPaths` includes relevant directories
3. Check virtual environment activated
4. Restart Pylance: `⌘ Shift P` → "Pylance: Restart Server"

### Format on Save Not Working

**Problem:** Black not formatting automatically

**Solution:**
1. Install Black Formatter extension
2. Verify settings:
   ```json
   "editor.formatOnSave": true,
   "[python]": {
       "editor.defaultFormatter": "ms-python.black-formatter"
   }
   ```
3. Check Black is installed: `pip install black` or `uv add black`

### File Exclusions Not Applied

**Problem:** `__pycache__` visible in explorer

**Solution:**
1. Verify `files.exclude` in settings
2. Reload window
3. Clear workspace cache: Delete `.vscode/.cache/`

---

## Recommended Workspace Settings

### For Python Projects

Create `.vscode/settings.json`:

```json
{
    "github.copilot.chat.codeGeneration.useInstructionFiles": true,
    "github.copilot.chat.scopeSelection": true,
    "chat.promptFilesLocations": {
        ".sia/prompts": true
    },
    "python.analysis.extraPaths": ["${workspaceFolder}"],
    "python.analysis.typeCheckingMode": "basic",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "editor.rulers": [88, 120],
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/htmlcov": true,
        "**/.coverage": true,
        "**/*.egg-info": true
    }
}
```

### For Multi-Language Projects

Add language-specific sections:

```json
{
    "[typescript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[javascript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[markdown]": {
        "editor.defaultFormatter": "yzhang.markdown-all-in-one"
    }
}
```

---

## Best Practices

### 1. Use Workspace Settings
- Commit `.vscode/settings.json` to repo
- Ensures team consistency
- SIA installer creates this automatically

### 2. Enable Copilot Instructions
- Always set `useInstructionFiles: true`
- Maintains Super Agent context
- Essential for SIA framework

### 3. Configure File Exclusions
- Hide build artifacts from explorer
- Improves search performance
- Reduces clutter

### 4. Set Up Rulers
- 88 chars for Python (Black default)
- 120 chars for max line length
- Visual guide for readability

### 5. Format on Save
- Consistent code style
- Reduces review comments
- Automatic cleanup

---

## Additional Resources

- **VS Code Docs:** https://code.visualstudio.com/docs
- **Copilot Docs:** https://docs.github.com/copilot
- **Python in VS Code:** https://code.visualstudio.com/docs/languages/python
- **SIA Framework:** `sia/README.md`

---

**See also:**
- `sia/docs/SLASH_COMMANDS.md` - Slash commands guide
- `sia/templates/vscode-settings.template.json` - Settings template
- `sia/QUICKSTART.md` - Framework quickstart
