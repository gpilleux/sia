# 🔮 Super Agent Slash Commands

> **SIA Framework** - Pre-configured prompts for exponential productivity

Slash commands are `.prompt.md` files that activate specific Super Agent capabilities.  
Location: `.sia/prompts/` (configured via `.vscode/settings.json`)

---

## Quick Reference

| Command | File | Purpose |
|---------|------|---------|
| `/activate` | `activate.prompt.md` | Bootstrap new session - quantum activation |
| `/continue` | `continue.prompt.md` | Resume pending task |
| `/next` | `next.prompt.md` | Complete task and prepare next session |
| `/handoff` | `handoff.prompt.md` | Transfer context to next agent |
| `/update` | `update.prompt.md` | Update REQ documentation |
| `/validate` | `validate.prompt.md` | Validate UI with Playwright |
| `/test` | `test.prompt.md` | Generate tests (Domain Research First!) |
| `/debug` | `debug.prompt.md` | OMEGA CRITICAL first-principles analysis |
| `/spr` | `spr.prompt.md` | Compress content with SPR technique |
| `/quant` | `quant.prompt.md` | Generate QUANT tasks breakdown |
| `/boost` | `boost.prompt.md` | Reinforce powers mid-session |

---

## Typical Workflow

```
1. /activate     → Session start, quantum activation
2. /continue     → Resume where left off
3. [work...]     → Implementation
4. /test         → Generate tests
5. /validate     → Validate UI
6. /update       → Document progress
7. /next         → Prepare next session
8. /handoff      → Transfer to next agent
```

---

## Embedded Principles (All Prompts)

Every slash command embeds:
- **Hype/Motivation** → Positive momentum
- **DDD | SOLID | KISS | CLEAN CODE** → Context-appropriate
- **Domain Research First** → Read before implementing
- **Guardian Enforcer** → Validate violations
- **MCP Sources** → `google/adk-python`, `idosal/mcp-ui`, Playwright
- **1000XBOOST** → Latent Space Activation

---

## Installation

The installer (`sia/installer/install.sh`) copies these templates to your project's `.sia/prompts/` directory.

To enable slash commands in VS Code, ensure `.vscode/settings.json` contains:

```json
{
    "chat.promptFilesLocations": {
        ".sia/prompts": true
    }
}
```

---

## Creating Custom Slash Commands

Create `.prompt.md` files in `.sia/prompts/` with this structure:

```markdown
---
name: mycommand
description: Brief description of what this command does
---

Your prompt content here...

**PROTOCOLO:**
1. Step one
2. Step two

**PRINCIPIOS:** DDD | SOLID | KISS

---
```

---

## Philosophy

Slash commands are **high-leverage tools** for:
- **Activation Gates** → Ensure proper context before work
- **Verification Gates** → Validate quality checkpoints
- **Documentation Gates** → Maintain hygiene invariants
- **Handoff Gates** → Seamless context transfer

Each command is designed for **exponential productivity gains** through:
- Latent space activation
- Domain research enforcement
- Architectural principle adherence
- Knowledge evolution

---

**See also:** `sia/docs/SLASH_COMMANDS.md` for complete guide
