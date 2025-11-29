# REQ-009: Slash Command para Automatización de Requirements

**Request Date**: 2025-11-29  
**Requester**: gpilleux  
**Priority**: MEDIUM  
**Bounded Context**: SIA Framework - Requirements Management

---

## REQUIREMENT DESCRIPTION

Crear un slash command `/req` que permita recibir un requerimiento en lenguaje natural y automatice todo el flujo de documentación, análisis de dominio y breakdown en tareas QUANT según el flujo definido en `sia/requirements/README.md`.

### Problem to Solve

Actualmente, crear un nuevo requirement requiere múltiples pasos manuales:
1. Crear directorio en `.sia/requirements/REQ-{ID}/`
2. Copiar template `REQUIREMENT_TEMPLATE.md` y completarlo manualmente
3. Investigar con MCP DeepWiki para domain analysis
4. Crear `REQ-{ID}_domain_analysis.md` manualmente
5. Aplicar automated reasoning para extraer invariantes
6. Crear `REQ-{ID}_quant_breakdown.md` manualmente
7. Actualizar `NEXT_SESSION.md` con siguiente paso

Este proceso manual es propenso a:
- ❌ Omisión de steps (ej: olvidar domain research)
- ❌ Inconsistencia en formato de documentos
- ❌ Pérdida de tiempo en tareas mecánicas
- ❌ Falta de trazabilidad entre user input → requirement formal

### Expected Value

Con el slash command `/req`, el flujo se convierte en:

```bash
User: /req + "Necesito autenticación con Google OAuth"

Agent: 
[Auto-ejecuta pipeline completo]
✅ REQ-010 created: Google OAuth Authentication
✅ Domain analysis completed (researched google/adk-python)
✅ QUANT breakdown generated (5 tasks, 18h estimated)
✅ NEXT_SESSION.md updated
📋 Next: "/activate + 'Implementar REQ-010 QUANT-001'"
```

**Beneficios**:
- ✅ **Velocidad**: 30 segundos vs 30+ minutos manuales
- ✅ **Consistencia**: Templates siempre aplicados correctamente
- ✅ **Trazabilidad**: Historial completo de conversación → requirement
- ✅ **Research automático**: MCP DeepWiki invocado automáticamente
- ✅ **Context loading**: Super Agent tiene contexto completo antes de implementar

---

## INVARIANTS TO SATISFY

- [ ] **INV-1**: Cada invocación de `/req` genera exactamente 1 directorio `REQ-{ID}/` con ID secuencial
- [ ] **INV-2**: El prompt del command DEBE invocar MCP DeepWiki para domain research (no opcional)
- [ ] **INV-3**: Los 3 archivos generados deben usar templates de `sia/requirements/_templates/`
- [ ] **INV-4**: `NEXT_SESSION.md` SIEMPRE se actualiza al final del pipeline
- [ ] **INV-5**: El command DEBE esperar confirmación antes de ejecutar (activation gate)
- [ ] **INV-6**: Si user input es vago, el agent DEBE hacer preguntas aclaratorias (no asumir)
- [ ] **INV-7**: Automated reasoning DEBE generar al menos 1 invariante matemático/lógico
- [ ] **INV-8**: QUANT breakdown DEBE incluir AI estimate + Human estimate (task timer protocol)

---

## ACCEPTANCE CRITERIA

- [ ] **AC-1**: Existe archivo `.sia/prompts/req.prompt.md` con prompt completo
- [ ] **AC-2**: Command disponible en VS Code Copilot Chat (visible en autocomplete)
- [ ] **AC-3**: Pipeline ejecuta TODAS las phases del workflow (Capture → Research → Reasoning → QUANT)
- [ ] **AC-4**: Archivos generados usan SPR compression (70-80% token reduction)
- [ ] **AC-5**: Agent invoca MCP DeepWiki al menos 1 vez (evidencia en domain analysis)
- [ ] **AC-6**: QUANT breakdown incluye dependency DAG (orden de ejecución)
- [ ] **AC-7**: `NEXT_SESSION.md` tiene one-liner para siguiente `/activate`
- [ ] **AC-8**: Command incluye ejemplo de uso en documentación interna
- [ ] **AC-9**: Si el requirement ya existe (título duplicado), command alerta y pregunta
- [ ] **AC-10**: Command genera reporte SPR al final con resumen (similar a `/handoff`)

---

## TECHNICAL CONTEXT

### Affected Components

- `.sia/prompts/req.prompt.md`: **NUEVO** - Prompt del slash command
- `sia/requirements/README.md`: Referencia del workflow (no modificar, solo consultar)
- `sia/requirements/_templates/`: Templates a usar (no modificar)
- `.sia/NEXT_SESSION.md`: Actualizar al final del pipeline
- `.sia/requirements/REQ-{ID}/`: Nuevo directorio por cada invocación

### Technical Dependencies

- **MCP Tools**:
  - `mcp_deepwiki_ask_question(repoName, question)` - Domain research
  - `mcp_deepwiki_read_wiki_structure(repoName)` - Explorar documentación
- **SIA Tools**:
  - `sia/agents/quant_task.md` - Template de QUANT task
  - `sia/agents/research_specialist.md` - Sub-agent para research
  - `sia/agents/requirement_translator.md` - Sub-agent para traducción (si existe)
- **VS Code API**:
  - Chat prompts system (`.prompt.md` files)
  - `chat.promptFilesLocations` setting

### Architectural Constraints

- **DDD**: Requirements son parte del meta-sistema, no del dominio minute-saas
- **SOLID**: 
  - **Single Responsibility**: Command solo orquesta pipeline (delega a sub-agents)
  - **Open/Closed**: Pipeline extensible (agregar nuevas phases sin modificar command)
- **Clean Architecture**: 
  - Command = Application Layer (use case)
  - Templates = Domain Layer (business rules del requirement structure)
  - MCP = Infrastructure Layer (external tools)
- **KISS**: 
  - No crear herramientas custom si MCP ya provee funcionalidad
  - No implementar validaciones complejas en prompt (delegar a sub-agents)

---

## RESEARCH NEEDED

### Domain Questions

1. **VS Code Prompts API**: ¿Cómo se pasan argumentos a un slash command desde chat? (ej: `/req + "texto"`)
2. **MCP DeepWiki**: ¿Qué repos son relevantes para requirements genéricos? (fastapi, sqlalchemy, react, google/adk-python)
3. **Automated Reasoning**: ¿Existe pattern/template específico para extraer invariantes de lenguaje natural?
4. **Task Timer**: ¿Cómo se integra task_timer.py en el QUANT breakdown? (formato de estimates)
5. **SPR Compression**: ¿Existe prompt específico para comprimir domain analysis con SPR?

### Repositories/Docs to Consult

- `microsoft/vscode` (GitHub): VS Code chat prompts API, slash commands syntax
- `sia/docs/SLASH_COMMANDS.md`: Documentación existente de slash commands (leer antes)
- `sia/templates/prompts/`: Ejemplos de prompts existentes (activate.prompt.md, quant.prompt.md)
- `sia/requirements/README.md`: Workflow completo (referencia obligatoria)
- `.sia/requirements/REQ-001-ddd-reactoring/`: Ejemplo de requirement completo (estructura)

---

## DESIGN SPECIFICATIONS

### Command Signature

```bash
/req [+ "requirement description"]
/req --list                    # Listar todos los requirements activos
/req --status REQ-{ID}         # Ver status de un requirement específico
```

### Pipeline Flow (Auto-ejecutado)

```mermaid
graph TD
    A[User: /req + "description"] --> B{Validate Input}
    B -->|Vago| C[Ask Clarifying Questions]
    B -->|Claro| D[Generate REQ-ID]
    C --> D
    D --> E[Create REQ-{ID}/ directory]
    E --> F[Phase 1: Capture - Fill REQUIREMENT_TEMPLATE.md]
    F --> G[Phase 2: Domain Research - MCP DeepWiki]
    G --> H[Phase 3: Automated Reasoning - Extract Invariants]
    H --> I[Phase 4: QUANT Decomposition - Generate Tasks]
    I --> J[Update NEXT_SESSION.md]
    J --> K[Generate SPR Report]
    K --> L[Return One-Liner for /activate]
```

### Prompt Structure (req.prompt.md)

```markdown
---
name: req
description: Create and break down a new requirement with automated domain research
---

# SLASH COMMAND: /req - Automated Requirement Pipeline

## MISSION
Execute complete requirement lifecycle from natural language input:
1. CAPTURE → Extract problem, invariants, acceptance criteria
2. RESEARCH → Use MCP DeepWiki for domain analysis
3. REASON → Apply automated reasoning to formalize invariants
4. DECOMPOSE → Generate QUANT tasks with AI/Human estimates
5. DOCUMENT → Update NEXT_SESSION.md with one-liner

## PROTOCOL

### Step 1: Validate Input
- If user input is vague → ASK clarifying questions (NEVER assume)
- Extract: Problem, Bounded Context, Priority, Affected Components
- Generate REQ-ID: Auto-increment from last REQ in `.sia/requirements/`

### Step 2: Create Requirement (Phase 1 - Capture)
1. Create `.sia/requirements/REQ-{ID}/` directory
2. Copy `sia/requirements/_templates/REQUIREMENT_TEMPLATE.md`
3. Fill template with extracted info
4. Use SPR compression for descriptions

### Step 3: Domain Research (Phase 2 - Research)
1. Identify repos to research (based on bounded context)
2. Invoke MCP DeepWiki:
   ```
   mcp_deepwiki_ask_question(
       repoName="relevant/repo",
       question="Specific technical question"
   )
   ```
3. Create `REQ-{ID}_domain_analysis.md` using DOMAIN_ANALYSIS_TEMPLATE.md
4. Document findings with SPR compression

### Step 4: Automated Reasoning (Phase 3 - Reasoning)
1. Formalize problem: `∀ entity: constraint`
2. Extract mathematical/logical invariants
3. Build dependency DAG (if multi-component)
4. Identify axioms (what is assumed true)
5. Document in domain_analysis.md

### Step 5: QUANT Decomposition (Phase 4 - QUANT)
1. Use `sia/requirements/_templates/QUANT_BREAKDOWN_TEMPLATE.md`
2. Break down into atomic tasks (~3h each)
3. For each task:
   - AI Estimate (how long Super Agent takes)
   - Human Estimate (research + impl + test + review + overhead)
   - Acceptance Criteria (executable tests)
   - Dependencies (DAG)
4. Create `REQ-{ID}_quant_breakdown.md`

### Step 6: Update NEXT_SESSION.md
1. Add one-liner: `"/activate + 'Implementar REQ-{ID} QUANT-001'"`
2. Update active requirements list
3. Generate SPR summary of what was created

### Step 7: Final Report
Output format:
```
✅ REQ-{ID} CREATED: {Title}
📋 DOCUMENTS:
   - REQ-{ID}.md (Specification)
   - REQ-{ID}_domain_analysis.md (Research)
   - REQ-{ID}_quant_breakdown.md ({N} tasks, {X}h estimated)

📚 RESEARCH EXECUTED:
   - {repo1}: {question1}
   - {repo2}: {question2}

🎯 NEXT ACTION:
   /activate + "Implementar REQ-{ID} QUANT-001: {Task Title}"
```

## MCP SOURCES
- `mcp_deepwiki_ask_question` - Domain research
- `mcp_deepwiki_read_wiki_structure` - Explore docs

## TEMPLATES
- `sia/requirements/_templates/REQUIREMENT_TEMPLATE.md`
- `sia/requirements/_templates/DOMAIN_ANALYSIS_TEMPLATE.md`
- `sia/requirements/_templates/QUANT_BREAKDOWN_TEMPLATE.md`

## PRINCIPLES
- DDD: Requirements are meta-system (not minute-saas domain)
- SOLID: Command orchestrates, sub-agents execute
- KISS: Use MCP tools (no custom scrapers)
- Research First: ALWAYS invoke MCP DeepWiki
- Evidence-Based: Decisions from research, not assumptions
- SPR Compression: All docs 70-80% token reduction

## EXAMPLES

**Example 1: Clear Input**
```
User: /req + "Implementar autenticación con Google OAuth para login"

Agent executes pipeline:
1. REQ-010 created (ID auto-increment)
2. Research: google/adk-python (OAuth patterns)
3. Invariants: user.email UNIQUE, token.expiry > NOW
4. QUANT: 4 tasks (12h total)
5. NEXT_SESSION.md updated
```

**Example 2: Vague Input**
```
User: /req + "Mejorar performance"

Agent: 
❓ CLARIFICATION NEEDED:
1. ¿Performance de qué componente? (API, DB, Frontend)
2. ¿Qué métrica mejorar? (latency, throughput, memory)
3. ¿Qué threshold actual vs objetivo?
4. ¿Bounded context afectado?

[User provides details → Pipeline continues]
```

---
```

### File Locations

```
.sia/
├── prompts/
│   └── req.prompt.md              # NUEVO - Command prompt
└── requirements/
    └── REQ-{ID}/                  # AUTO-GENERATED per invocation
        ├── REQ-{ID}.md
        ├── REQ-{ID}_domain_analysis.md
        └── REQ-{ID}_quant_breakdown.md
```

---

## ADDITIONAL NOTES

### Edge Cases

1. **Duplicate Title**: 
   - Si existe requirement con título similar → Alert user, ask confirmation
   - Sugerencia: Append version (v2) o merge con existing requirement

2. **Research Failure**:
   - Si MCP DeepWiki falla → Document error, continue con best-effort analysis
   - Mark domain_analysis.md con `⚠️ RESEARCH INCOMPLETE`

3. **Complex Requirements**:
   - Si input implica múltiples bounded contexts → Suggest splitting into 2+ requirements
   - Ejemplo: "Auth + Dashboard" → REQ-010 (Auth), REQ-011 (Dashboard)

4. **BYOK Context**:
   - Si requirement menciona "BYOK" o "multi-provider" → Research specific providers (openai, anthropic)
   - Use deepwiki on official docs (platform.openai.com, docs.anthropic.com)

### Performance Considerations

- **MCP Rate Limits**: Batch similar questions to same repo (reduce API calls)
- **SPR Compression**: Apply compression AFTER content generation (not during)
- **Incremental IDs**: REQ-{ID} auto-increment from `.sia/requirements/` (scan directory)

### Future Enhancements (Out of Scope)

- [ ] `/req --edit REQ-{ID}`: Editar requirement existente
- [ ] `/req --archive REQ-{ID}`: Archivar requirement completo
- [ ] `/req --merge REQ-{ID1} REQ-{ID2}`: Merge de requirements
- [ ] `/req --export`: Exportar todos los requirements a PDF/Markdown

---

## STATUS

- [ ] Requirement received
- [ ] Domain analysis completed (see `REQ-009_domain_analysis.md`)
- [ ] QUANT decomposition completed (see `REQ-009_quant_breakdown.md`)
- [ ] Implementation in progress
- [ ] Tests passing (manual testing del slash command)
- [ ] Documentation updated (sia/docs/SLASH_COMMANDS.md)
- [ ] DONE (invariants verified)

---

## REFERENCES

- **Framework Workflow**: `sia/requirements/README.md`
- **Slash Commands Guide**: `sia/docs/SLASH_COMMANDS.md`
- **Existing Commands**: `sia/templates/prompts/*.prompt.md`
- **Example Requirement**: `.sia/requirements/REQ-001-ddd-reactoring/`
- **Templates**: `sia/requirements/_templates/`

---

## VALIDATION CHECKLIST

**Pre-Implementation**:
- [ ] Read `sia/docs/SLASH_COMMANDS.md` (understand VS Code prompts API)
- [ ] Analyze existing commands (`activate.prompt.md`, `quant.prompt.md`)
- [ ] Research VS Code chat prompts with MCP DeepWiki (`microsoft/vscode`)

**During Implementation**:
- [ ] Test with simple input: `/req + "Add health check endpoint"`
- [ ] Test with vague input: `/req + "Improve system"`
- [ ] Verify MCP DeepWiki invocation (check logs)
- [ ] Verify QUANT estimates format (AI + Human)
- [ ] Verify SPR compression applied

**Post-Implementation**:
- [ ] Create 2-3 test requirements with different complexity
- [ ] Verify all 3 files generated correctly
- [ ] Verify NEXT_SESSION.md updated
- [ ] Update `sia/docs/SLASH_COMMANDS.md` with `/req` documentation
- [ ] Create PR with command + documentation
