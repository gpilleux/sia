# Sub-Agent Delegation Analysis & Proposal
**SIA Framework - Native VS Code Copilot Integration**

## RESUMEN EJECUTIVO

### Hallazgos Clave

**Situación actual**: 
- Agentes SIA son documentación markdown (`.sia/agents/*.md`)
- Delegación es conceptual/simulada (SUPER_AGENT lee `.md` y ejecuta lógica manualmente)
- No hay invocación real de sub-agentes

**Descubrimiento**:
- VS Code Copilot tiene `runSubagent` tool (nativo, interno)
- Soporta custom agents vía `.github/agents/*.agent.md`
- Permite delegación asíncrona con contexto compartido

**Propuesta**:
- Convertir agentes SIA a custom agents ejecutables
- SUPER_AGENT delega vía `runSubagent` (no simula)
- Sub-agents retornan markdown SPR para integración

**Prototipo**:
- ✅ Research Specialist custom agent creado (`.github/agents/research-specialist.agent.md`)
- ✅ Validación de atributos soportados (solo `name`, `description`, `target`, `tools`)
- ✅ Arquitectura propuesta documentada (5 fases de implementación)

**Siguiente paso**: Formalizar en REQ-XXX + ejecutar QUANT-001 (validar prototipo)

---

## ESTADO ACTUAL

### Arquitectura Existente

**Archivos clave**:
- `agents/*.md` - 7 agentes especializados (Repository Guardian, Research Specialist, SIA, etc.)
- `skills/create_agent_cli.py` - CLI para creación de agentes expertos
- `skills/create_expert_agent.md` - Metodología 7-phase workflow
- `.github/copilot-instructions.md` - Instrucciones SUPER_AGENT

**Delegación actual**: Conceptual (markdown-based)
```markdown
## DELEGATION PROTOCOL

**Escalate to [Agent Name]** when:
- [Condition 1]
- [Condition 2]
```

**Problema**: Los sub-agentes NO se invocan realmente. Son documentación pasiva que el SUPER_AGENT "simula" leyendo los archivos `.md` y ejecutando la lógica manualmente.

---

## INVESTIGACIÓN: RUNSUBAGENT EN VS CODE

### Descubrimientos Clave (DeepWiki - microsoft/vscode)

#### 1. runSubagent Tool (Nativo de VS Code)

**Capacidades**:
- Delegación asíncrona de tareas complejas multi-paso
- Contexto compartido vía `sessionId` y `sessionResource`
- Output streaming (progress + markdown results)
- Sub-agente retorna `IToolResult` con markdown concatenado

**Protocolo de invocación** (LLM → runSubagent):
```json
{
  "tool": "runSubagent",
  "parameters": {
    "prompt": "Detailed task description with context",
    "description": "Short 3-5 word task name",
    "agentName": "OptionalCustomAgent"  // Requires chat.subagentTool.customAgents
  }
}
```

**Flujo interno**:
```
Parent Agent invoca runSubagent
    ↓
runSubagent crea IChatAgentRequest {
    sessionId, sessionResource,  // Contexto compartido
    message: prompt,
    isSubagent: true,            // Flag para sub-agent
    userSelectedModelId,         // Opcional (custom agent)
    userSelectedTools            // Opcional (custom agent)
}
    ↓
IChatAgentService.invokeAgent(request, progressCallback)
    ↓
Sub-agent ejecuta (async)
    ↓
Progress → callback recibe IChatProgress[] parts:
    - markdownContent → collected
    - textEdit/notebookEdit → accepted
    - prepareToolInvocation → forwarded
    ↓
Sub-agent completa → retorna IChatAgentResult
    ↓
runSubagent retorna IToolResult {
    markdown: concatenated markdownParts
}
```

**Limitaciones observadas**:
- `agentName` requiere `chat.subagentTool.customAgents` enabled
- Custom agents se cargan de `.github/agents/*.agent.md`
- No hay API pública de extensión (internal tool)

#### 2. Custom Agents (ICustomAgent)

**Formato de configuración** (`.github/agents/<name>.agent.md`):
```yaml
---
name: research-specialist
description: Knowledge discovery and pattern research
target: github-copilot
tools:
  - mcp_deepwiki_ask_question
  - mcp_repo-indexer_search_code
  - semantic_search
---

# ⚠️ IMPORTANTE: Atributos soportados por VS Code
# Según validación real, solo estos atributos son válidos:
# - name: Identificador del agente
# - description: Descripción breve
# - target: github-copilot (siempre)
# - tools: Array de herramientas MCP/built-in
# - mcp-servers: (opcional) servidores MCP específicos
#
# NO soportados (ignorados o causan error):
# - model: (selección de modelo se hace en VS Code settings)
# - argumentHint: (no es parte del spec)
# - handOffs: (pendiente de confirmación)

# Research Specialist Agent Instructions

You are a knowledge discovery specialist. Your mission is...

[Agent SPR content]
```

**Propiedades clave** (`ICustomAgent` - según código VS Code):
- `name` - Identificador del agente
- `description` - Descripción breve
- `tools[]` - Herramientas MCP/built-in disponibles
- `agentInstructions.content` - Markdown con instrucciones SPR
- `handOffs` - Delegación entre agentes (NO confirmado en spec actual)
- `source` - Origen (local, user, extension)

**Propiedades VS Code validadas** (frontmatter soportado):
- ✅ `name`
- ✅ `description`
- ✅ `target` (siempre "github-copilot")
- ✅ `tools`
- ✅ `mcp-servers` (opcional)
- ❌ `model` (NO soportado - se configura en VS Code settings)
- ❌ `argumentHint` (NO soportado - no es parte del spec)

**Lifecycle**:
```
IPromptsService descubre .github/agents/*.agent.md
    ↓
Parsea YAML frontmatter + markdown body
    ↓
IChatModeService registra como CustomChatMode
    ↓
Disponible para runSubagent vía agentName parameter
```

---

## DISEÑO PROPUESTO: SIA NATIVE DELEGATION

### Objetivos

1. **Delegación real** (no simulada) - SUPER_AGENT invoca sub-agentes vía `runSubagent`
2. **Contexto preservado** - Session state compartido entre SUPER_AGENT ↔ sub-agent
3. **Herramientas especializadas** - Cada sub-agent tiene acceso a MCP tools específicos
4. **Output estructurado** - Sub-agent retorna markdown con formato SPR
5. **Elegancia nativa** - Usa capacidades de VS Code sin hacks

### Arquitectura Propuesta

#### Estructura de archivos

```
.github/
└── agents/
    ├── repository_guardian.agent.md
    ├── research_specialist.agent.md
    ├── compliance_officer.agent.md
    ├── sia_ddd.agent.md
    └── microsoft_suite_specialist.agent.md

.sia/
└── agents/
    ├── repository_guardian.md        # Legacy (docs)
    ├── research_specialist.md        # Legacy (docs)
    └── [project_name].md            # Project SPR
```

**Razonamiento**:
- `.github/agents/*.agent.md` - Agentes EJECUTABLES (VS Code native)
- `.sia/agents/*.md` - Documentación SPR (referencia, evolución)
- Project SPR permanece en `.sia/agents/` (específico del proyecto)

#### Template: Custom Agent File

**Ejemplo**: `.github/agents/research_specialist.agent.md`

```yaml
---
name: research-specialist
description: Knowledge discovery specialist (MCP Deepwiki + Repo-Indexer)
target: github-copilot
model: gpt-4o
tools:
  - mcp_deepwiki_ask_question
  - mcp_deepwiki_read_wiki_contents
  - mcp_repo-indexer_search_code
  - semantic_search
  - grep_search
argumentHint: "[research topic or repo name]"
---

# Research Specialist Agent

## LATENT SPACE ACTIVATION (LSA)

**Cognitive Priming Vectors**:
- Targeted research protocol (question formulation → execution → synthesis)
- MCP Deepwiki patterns (ask_question > read_wiki_contents)
- Token budget optimization (minimize context usage)
- Incremental deepening (shallow → deep, exit early)

**Problem-Solving Patterns**:
- Unknown implementation → "Does [framework] support [feature]? Show example."
- Pattern discovery → "In [repo], how to [task] with [constraints]? Code snippet."
- Edge cases → "How to handle [scenario] in [framework]? Show error handling."

---

## CORE MISSION

Expert in **knowledge discovery** using MCP Deepwiki and Repo-Indexer. 
Formulate **targeted questions** to minimize token usage. 
Synthesize findings into **actionable SPR summaries**.

**Anti-Pattern**: ❌ Never use `read_wiki_structure` + loop over topics (context explosion)

---

## EXPERTISE

### MCP Deepwiki Mastery
- **Question formulation**: Context + Need + Question + Expected Output
- **Repository selection**: Primary repo (specific question) vs exhaustive research
- **Incremental deepening**: Layer 1 (verify) → Layer 2 (details) → Layer 3 (edge cases)

### Research Synthesis
- **Pattern extraction**: 5+ core patterns per research session
- **Anti-pattern detection**: 3+ documented "what NOT to do"
- **Code examples**: Executable snippets with context
- **Token efficiency**: Target <5000 tokens total (vs 25k+ full wiki)

---

## WORKFLOW

### Phase 1: Question Formulation (Pre-Research)

**Template**:
```markdown
Context: [What I'm implementing]
Need: [Specific information gap]
Question: [Precise query with constraints]
Expected Output: [code | pattern | config | tools]
```

**Example** (Good ✅):
```
Context: Implementing multi-turn chat with function calling
Need: Understand state persistence during streaming
Question: In LangChain, how to persist chat history during streaming 
          function calls? Show AsyncChatMessageHistory pattern.
Expected Output: Code snippet showing session persistence + streaming integration
```

### Phase 2: Execute Research (MCP-First)

**Primary tool**: `mcp_deepwiki_ask_question(repo, question)`

**Strategy**:
1. Start with primary repo (most specific)
2. If insufficient → formulate follow-up question
3. If still insufficient → query secondary repo
4. Exit early when answer complete (preserve context)

### Phase 3: Synthesize Results (SPR Format)

**Output structure**:
```markdown
## RESEARCH FINDINGS

### MCP Queries Executed
1. `repo/name` - "question" → Finding: [concise summary]
2. `repo/name` - "question" → Finding: [concise summary]

### Patterns Discovered
- **[Pattern Name]**: [Brief description + use case]

### Anti-Patterns
- ❌ [Anti-pattern]: [Why it fails]

### Code Examples
\`\`\`language
[Executable snippet with comments]
\`\`\`

### Tokens Used
- Total: ~X tokens (vs ~Y tokens full wiki)
- Efficiency: Z% context preserved
```

---

## VERIFICATION CHECKLIST

Before returning results:
- ✅ Queried MCP Deepwiki (not simulated)
- ✅ Questions were specific (not "how does X work?")
- ✅ Extracted 3+ patterns or 1+ code example
- ✅ Identified anti-patterns (what NOT to do)
- ✅ Token usage < 5000 total
- ✅ Output format matches SPR structure

---

## DELEGATION PROTOCOL

**Escalate to Repository Guardian** when:
- Research findings require DDD compliance verification
- Architecture patterns need validation

**Escalate to SIA Agent** when:
- Research findings require ADK/TimescaleDB implementation
- AI-Native patterns need integration

---

**Agent Version**: 2.0.0 (Native VS Code Integration)  
**MCP Dependencies**: deepwiki, repo-indexer  
**Last Updated**: 2025-11-30  
**Status**: ✅ Production Ready
```

#### Conversión de Agentes Existentes

**Mapping**: `.sia/agents/*.md` → `.github/agents/*.agent.md`

| Existing Agent                  | Custom Agent File                     | Tools                                                     | Notes              |
| ------------------------------- | ------------------------------------- | --------------------------------------------------------- | ------------------ |
| `research_specialist.md`        | `research-specialist.agent.md`        | `mcp_deepwiki_*`, `mcp_repo-indexer_*`, `semantic_search` | ✅ Prototipo creado |
| `repository_guardian.md`        | `repository-guardian.agent.md`        | `run_in_terminal`, `get_errors`, `list_code_usages`       | Pending            |
| `compliance_officer.md`         | `compliance-officer.agent.md`         | `read_file`, `create_file`, `replace_string_in_file`      | Pending            |
| `sia.md`                        | `sia-ddd.agent.md`                    | `mcp_deepwiki_*`, `read_file`, `semantic_search`          | Pending            |
| `microsoft_suite_specialist.md` | `microsoft-suite-specialist.agent.md` | `mcp_learn_*`, `mcp_microsoft-365_*`                      | Pending            |

**Nota sobre `model`**:
- Atributo `model` NO es soportado en frontmatter
- Selección de modelo se hace en VS Code settings globales
- Todos los custom agents usan el modelo configurado por defecto
- Trade-off aceptado: No podemos optimizar modelo por agente (como planeado originalmente)

**Preservación**:
- `.sia/agents/*.md` permanecen como documentación SPR (referencia)
- `.github/agents/*.agent.md` son versiones EJECUTABLES (VS Code native)
- Sincronización manual (o script) cuando agente evoluciona

---

### Protocolo de Comunicación

#### 1. SUPER_AGENT → Sub-Agent (Invocation)

**Contexto SUPER_AGENT** (en `.github/copilot-instructions.md`):

```markdown
## DELEGATION MODEL

**Sub-Agents** (Native VS Code Custom Agents):
- `research-specialist` - Knowledge discovery (MCP Deepwiki + Repo-Indexer)
- `repository-guardian` - DDD/SOLID enforcement, skills execution
- `compliance-officer` - Requirements validation, QUANT lifecycle
- `sia-ddd` - AI-Native patterns (ADK, TimescaleDB, SSE)
- `microsoft-suite-specialist` - M365 expertise (SharePoint, Graph API)

**Invocation Pattern**:
```
User Request → SUPER_AGENT analyzes
    ↓
Decision: Delegate? (bounded context match)
    ↓
Invoke runSubagent:
    prompt: "[Detailed task with context + constraints + expected output]"
    description: "Short task name"
    agentName: "[sub-agent-name]"
    ↓
Sub-agent executes (async, shared session context)
    ↓
Sub-agent returns markdown (SPR format)
    ↓
SUPER_AGENT validates + integrates results
    ↓
Update Project SPR (.sia/agents/[project].md)
```

**Ejemplo de delegación**:

```markdown
User: "Investiga cómo implementar vector search con pgvector en LangChain"

SUPER_AGENT analiza:
- Bounded Context: Research (external knowledge)
- Complexity: Medium (requiere Deepwiki queries)
- Decision: Delegate to research-specialist

SUPER_AGENT invoca:
```json
{
  "tool": "runSubagent",
  "parameters": {
    "prompt": "Research pgvector integration in LangChain. Context: Building semantic code search with embeddings. Need: Implementation patterns for pgvector + LangChain with async support. Questions: 1) How to configure PGVector as vector store in LangChain? 2) How to handle batch embeddings with connection pooling? 3) Best practices for index optimization. Expected Output: Code examples + patterns + anti-patterns. Repos: langchain-ai/langchain, pgvector/pgvector.",
    "description": "LangChain pgvector integration",
    "agentName": "research-specialist"
  }
}
```

Research Specialist ejecuta → retorna SPR markdown:
```markdown
## RESEARCH FINDINGS

### MCP Queries Executed
1. `langchain-ai/langchain` - "How to configure PGVector..." → [Finding]
2. `pgvector/pgvector` - "Best practices for index..." → [Finding]

### Patterns Discovered
- **Async Connection Pooling**: [Pattern]
- **Batch Embedding**: [Pattern]

### Code Examples
[Executable snippets]

### Tokens Used: 2,300 (vs 28,000 full wiki)
```

SUPER_AGENT integra:
- Valida findings
- Actualiza `.sia/agents/[project].md` con patterns
- Responde al usuario con síntesis
```

#### 2. Sub-Agent → Sub-Agent (Handoffs)

**Escenario**: Research Specialist descubre violación DDD → Escalate to Repository Guardian

**Implementación** (en `research_specialist.agent.md`):

```yaml
---
handOffs:
  - agent: repository-guardian
    when: "Research findings require DDD compliance verification"
  - agent: sia-ddd
    when: "Patterns require AI-Native implementation guidance"
---
```

**Protocolo**:
```
Research Specialist completa research
    ↓
Detecta: "Pattern involves domain layer changes"
    ↓
Returns markdown con handoff metadata:
```markdown
## FINDINGS

[Research results]

## RECOMMENDED HANDOFF

**To**: `repository-guardian`
**Reason**: Proposed pattern modifies domain layer (DDD validation required)
**Context**: [Specific findings that need validation]
```
    ↓
SUPER_AGENT procesa handoff
    ↓
Invoca runSubagent(agentName="repository-guardian", prompt=...)
```

---

### Ventajas de la Arquitectura Propuesta

#### 1. Delegación Real (No Simulada)

**Antes** (Conceptual):
```markdown
# .github/copilot-instructions.md
"Delegate to Repository Guardian by reading agents/repository_guardian.md 
and executing its logic"
```
→ SUPER_AGENT simula sub-agent leyendo archivo y ejecutando manualmente

**Después** (Native):
```json
{
  "tool": "runSubagent",
  "parameters": {
    "agentName": "repository-guardian",
    "prompt": "[Task with context]"
  }
}
```
→ VS Code invoca custom agent con herramientas especializadas

#### 2. Contexto Compartido (Session State)

**Problema actual**: Sub-agent no tiene contexto de sesión
**Solución propuesta**: `runSubagent` pasa `sessionId` y `sessionResource`

**Beneficio**:
- Sub-agent accede a historial de chat
- Puede referenciar mensajes anteriores
- Mantiene coherencia en multi-turn delegation

#### 3. Herramientas Especializadas

**Ejemplo**: Research Specialist

**Antes**:
- SUPER_AGENT tiene acceso a TODAS las herramientas
- Research Specialist es simulado (no puede invocar MCP directamente)

**Después**:
```yaml
# .github/agents/research_specialist.agent.md
tools:
  - mcp_deepwiki_ask_question
  - mcp_repo-indexer_search_code
  - semantic_search
```
→ Research Specialist invoca MCP directamente, SUPER_AGENT NO necesita simular

#### 4. Output Estructurado (SPR Format)

**Antes**: Output mezclado con lógica de SUPER_AGENT
**Después**: Sub-agent retorna markdown SPR → SUPER_AGENT integra cleanly

**Ejemplo**:
```markdown
## RESEARCH FINDINGS
[Structured SPR output from sub-agent]

## SUPER_AGENT INTEGRATION
[SUPER_AGENT adds project-specific context]
```

#### 5. Elegancia Nativa

**Sin hacks**:
- No custom API server
- No webhook listeners
- No file-based message passing
- No polling loops

**Solo** VS Code native features:
- `runSubagent` tool (built-in)
- Custom agents (`.github/agents/*.agent.md`)
- MCP tools (via tools: [])
- Session state (via sessionId)

---

## PLAN DE IMPLEMENTACIÓN

### Fase 1: Prototipo (Single Agent)

**QUANT-001**: Convertir Research Specialist a custom agent

**Tareas**:
1. Crear `.github/agents/research_specialist.agent.md`
   - Copiar SPR content de `.sia/agents/research_specialist.md`
   - Agregar YAML frontmatter (name, tools, model)
   - Adaptar formato para VS Code custom agent

2. Habilitar custom agents en VS Code
   - `"chat.subagentTool.customAgents": true` (settings.json)
   - Reload window

3. Probar invocación desde SUPER_AGENT
   - Instrucción en `.github/copilot-instructions.md`:
     ```markdown
     When research is needed, invoke:
     runSubagent(agentName="research-specialist", prompt="[detailed task]")
     ```

4. Validar output
   - Sub-agent retorna markdown SPR
   - SUPER_AGENT integra findings
   - No errors/warnings en console

**Criterios de éxito**:
- ✅ Custom agent visible en VS Code
- ✅ SUPER_AGENT puede invocar runSubagent
- ✅ Research Specialist ejecuta MCP queries
- ✅ Output formato SPR correcto

### Fase 2: Multi-Agent System

**QUANT-002**: Convertir todos los agentes core

**Agentes a convertir**:
1. `repository_guardian.agent.md`
2. `compliance_officer.agent.md`
3. `sia_ddd.agent.md`

**Tareas por agente**:
1. Crear `.github/agents/[name].agent.md`
2. Mapear herramientas (tools: [])
3. Seleccionar modelo (model: gpt-4 | gpt-4o)
4. Definir handoffs (handOffs: [])
5. Probar invocación aislada
6. Probar handoff chain

**Criterios de éxito**:
- ✅ 4 agentes convertidos (research, guardian, compliance, sia-ddd)
- ✅ Cada agente ejecutable independientemente
- ✅ Handoffs funcionan (research → guardian → sia-ddd)
- ✅ No duplicación de lógica SUPER_AGENT ↔ sub-agent

### Fase 3: SUPER_AGENT Orchestration

**QUANT-003**: Actualizar SUPER_AGENT para delegación nativa

**Cambios en `.github/copilot-instructions.md`**:

**Antes**:
```markdown
## DELEGATION MODEL

**Invocation Pattern**:
User Request → SUPER_AGENT analyzes → Reads sub-agent .md file → Executes logic manually
```

**Después**:
```markdown
## DELEGATION MODEL

**Sub-Agents** (Native Custom Agents):
- `research-specialist` - [Description + tools + when to invoke]
- `repository-guardian` - [Description + tools + when to invoke]
- `compliance-officer` - [Description + tools + when to invoke]
- `sia-ddd` - [Description + tools + when to invoke]

**Invocation Protocol**:
```typescript
// When bounded context matches sub-agent expertise:
runSubagent({
  agentName: "[sub-agent-name]",
  prompt: "[Detailed task with context + constraints + expected output format]",
  description: "[Short 3-5 word task name]"
})

// Sub-agent executes → returns markdown (SPR format)
// SUPER_AGENT validates → integrates → updates Project SPR
```

**Decision Tree**:
| User Request Type               | Delegate To                  | Reason                        |
| ------------------------------- | ---------------------------- | ----------------------------- |
| "Research [framework] patterns" | `research-specialist`        | External knowledge (Deepwiki) |
| "Validate DDD compliance"       | `repository-guardian`        | Architecture enforcement      |
| "Create requirement REQ-XXX"    | `compliance-officer`         | Requirements management       |
| "Implement ADK agent"           | `sia-ddd`                    | AI-Native patterns            |
| "SharePoint configuration"      | `microsoft-suite-specialist` | M365 expertise                |
```

**Tareas**:
1. Documentar decision tree (bounded context → sub-agent)
2. Definir prompt templates para cada delegación
3. Especificar expected output format (SPR structure)
4. Probar delegation flows:
   - User request → Research Specialist
   - Research → Repository Guardian (handoff)
   - User request → Compliance Officer → SIA DDD (handoff)

**Criterios de éxito**:
- ✅ SUPER_AGENT delega correctamente (no simula)
- ✅ Prompts contienen contexto suficiente
- ✅ Sub-agents retornan SPR format consistente
- ✅ Handoffs funcionan sin intervención SUPER_AGENT

### Fase 4: Skill Integration (Custom Agent + runInTerminal)

**QUANT-004**: Integrar skills SIA con Repository Guardian

**Problema**: Skills ejecutan bash scripts (e.g., `check_complexity.sh`)
**Solución**: Repository Guardian invoca `run_in_terminal` tool

**Cambios en `repository_guardian.agent.md`**:

```yaml
---
tools:
  - run_in_terminal
  - get_errors
  - list_code_usages
  - read_file
  - semantic_search
---

## SKILLS EXECUTION

### Complexity Analysis
When user requests: "Check code complexity"

```typescript
run_in_terminal({
  command: "bash sia/skills/check_complexity.sh",
  explanation: "Analyzing cyclomatic complexity with Radon"
})

// Parse output → Extract violations → Format as SPR markdown
```

### DDD Compliance Audit
```typescript
run_in_terminal({
  command: "python sia/skills/audit_ddd.py --strict",
  explanation: "Validating Domain-Driven Design layer separation"
})

// Parse output → Identify violations → Recommend fixes
```
```

**Tareas**:
1. Definir skill invocation patterns en agent instructions
2. Probar ejecución: SUPER_AGENT → Repository Guardian → run_in_terminal → skill script
3. Validar output parsing (bash stdout → markdown SPR)
4. Documentar error handling (skill fails → agent reports gracefully)

**Criterios de éxito**:
- ✅ Repository Guardian ejecuta skills vía run_in_terminal
- ✅ Output parseado correctamente (violations, metrics)
- ✅ Errors manejados (script fails → meaningful error message)

### Fase 5: Documentation & Tooling

**QUANT-005**: Documentar arquitectura + crear migration script

**Deliverables**:

1. **ArquitecturaDoc** (`docs/SUBAGENT_ARCHITECTURE.md`):
   - Diagrama: SUPER_AGENT ↔ Custom Agents ↔ MCP Tools
   - Lifecycle: User Request → Delegation → Execution → Integration
   - Protocols: Invocation, Handoffs, Output Format
   - Examples: Real delegation flows

2. **Migration Script** (`installer/convert_agents.py`):
   ```python
   # Convert .sia/agents/*.md → .github/agents/*.agent.md
   # Extract SPR content + generate YAML frontmatter
   # Map tools based on agent expertise
   # Select model (gpt-4 vs gpt-4o)
   ```

3. **Testing Guide** (`docs/TESTING_SUBAGENTS.md`):
   - How to test custom agent in isolation
   - How to validate handoffs
   - How to debug delegation issues
   - Example test cases

**Criterios de éxito**:
- ✅ Documentation complete (architecture + migration + testing)
- ✅ Migration script converts agents correctly
- ✅ Testing guide includes 5+ example test cases

---

## DECISIONES DE DISEÑO

### 1. ¿Por qué `.github/agents/*.agent.md` y NO `.sia/agents/`?

**Razones**:
- VS Code busca custom agents en `.github/agents/` por convención
- `.sia/agents/` es directorio SIA-specific (framework)
- Separación de concerns:
  - `.github/agents/` - Agentes EJECUTABLES (VS Code)
  - `.sia/agents/` - Documentación SPR (referencia, evolución)

**Trade-off aceptado**:
- Duplicación parcial de contenido (SPR instructions)
- Sincronización manual cuando agente evoluciona

**Mitigación**:
- Script `installer/sync_agents.py` (one-way: `.sia/agents/*.md` → `.github/agents/*.agent.md`)
- Agente evoluciona en `.sia/agents/*.md` (source of truth)
- Re-generación de `.github/agents/*.agent.md` vía script

### 2. ¿Modelo único o específico por agente?

**Decisión (Actualizada tras validación)**: Modelo único (configurado en VS Code settings)

**Razonamiento**:
- Atributo `model` en frontmatter NO es soportado por VS Code
- Selección de modelo se hace globalmente en settings.json:
  ```json
  {
    "github.copilot.advanced": {
      "chatModel": "gpt-4o"
    }
  }
  ```
- Todos los custom agents usan el mismo modelo

**Trade-off aceptado**:
- ❌ No podemos optimizar modelo por agente (plan original)
- ✅ Simplicidad de configuración (un solo modelo)
- ✅ Costo predecible (no mixtura gpt-4 + gpt-4o)

**Plan original descartado**:
```yaml
# Esto NO funciona (model no soportado)
---
name: research-specialist
model: gpt-4o  # ❌ Ignorado por VS Code
---
```

**Workaround futuro** (si necesario):
- Crear agentes separados con settings.json diferentes
- O esperar a que VS Code soporte `model` en frontmatter

### 3. ¿Handoffs automáticos o SUPER_AGENT orchestration?

**Decisión**: Hybrid approach

**Automáticos** (handOffs in agent frontmatter):
- Research Specialist → Repository Guardian (when DDD validation needed)
- Repository Guardian → Compliance Officer (when violations require REQ)

**Orchestrated** (SUPER_AGENT decision):
- Complex workflows (REQ creation → Research → Implementation → Validation)
- Multi-step QUANT tasks (Phase 1 → Phase 2 → Phase 3)

**Razonamiento**:
- Simple handoffs: Declarative (YAML handOffs)
- Complex orchestration: Programmatic (SUPER_AGENT logic)

### 4. ¿Qué pasa con el Project SPR (`.sia/agents/[project].md`)?

**Decisión**: Project SPR NO es custom agent

**Razonamiento**:
- Project SPR = Arquitectura específica del proyecto (no reusable)
- Custom agents = Capacidades genéricas (reusables across projects)

**Ejemplo**:
- `research_specialist.agent.md` - Reusable (cualquier proyecto)
- `.sia/agents/erp.md` - Específico (solo proyecto ERP)

**Uso**:
- SUPER_AGENT lee Project SPR (contexto arquitectónico)
- SUPER_AGENT delega a custom agents (capacidades especializadas)
- Custom agents NO leen Project SPR directamente (contexto viene en prompt)

---

## RIESGOS & MITIGACIONES

### Riesgo 1: Custom agents requieren flag experimental

**Problema**: `chat.subagentTool.customAgents` puede ser deprecado/cambiado
**Probabilidad**: Media
**Impacto**: Alto (arquitectura propuesta depende de esto)

**Mitigación**:
- Monitorear VS Code release notes (custom agents roadmap)
- Fallback plan: Si feature deprecada → volver a markdown-based delegation
- Mantener `.sia/agents/*.md` como source of truth (fácil rollback)

### Riesgo 2: Performance overhead (runSubagent latency)

**Problema**: Cada delegación crea nueva sesión de chat (latency adicional)
**Probabilidad**: Baja
**Impacto**: Medio (user experience degradada)

**Mitigación**:
- Delegar solo cuando necesario (decision tree estricto)
- Consolidar múltiples sub-tareas en single prompt (batch operations)
- Medir latency (research → compare vs manual execution)

### Riesgo 3: Context overflow (sub-agent + SUPER_AGENT context)

**Problema**: Sub-agent genera output largo → SUPER_AGENT context explodes
**Probabilidad**: Media
**Impacto**: Alto (context window exceeded)

**Mitigación**:
- Enforce SPR format (compression protocol)
- Sub-agent verification checklist: "Output < 5000 tokens"
- SUPER_AGENT summarizes sub-agent output before storing (lossy compression)

### Riesgo 4: Handoff loops (agent A → agent B → agent A)

**Problema**: Handoffs mal configurados crean loops infinitos
**Probabilidad**: Baja
**Impacto**: Crítico (sistema hang)

**Mitigación**:
- Handoffs unidireccionales (DAG, no ciclos)
- Max handoff depth = 2 (A → B → C, stop)
- SUPER_AGENT detecta loop (track delegation history)

---

## MÉTRICAS DE ÉXITO

### Fase 1 (Prototipo)
- ✅ Research Specialist custom agent creado
- ✅ SUPER_AGENT invoca runSubagent exitosamente
- ✅ Sub-agent ejecuta MCP queries (Deepwiki)
- ✅ Output formato SPR correcto

### Fase 2 (Multi-Agent)
- ✅ 4 agentes core convertidos
- ✅ 3+ handoffs probados exitosamente
- ✅ No errors en VS Code console

### Fase 3 (Orchestration)
- ✅ SUPER_AGENT delega 80%+ tareas correctamente
- ✅ Decision tree documentado (bounded context → agent)
- ✅ 5+ delegation flows probados end-to-end

### Fase 4 (Skills Integration)
- ✅ Repository Guardian ejecuta skills vía run_in_terminal
- ✅ 3+ skills probados (complexity, coverage, ddd audit)
- ✅ Output parsing correcto (violations → SPR markdown)

### Fase 5 (Documentation)
- ✅ Arquitectura documentada (diagrams + protocols)
- ✅ Migration script funcional (conversion rate 100%)
- ✅ Testing guide con 5+ test cases

---

## NEXT STEPS

### Inmediato (Esta sesión)
1. ✅ Análisis completado (este documento)
2. ⏭️ Crear REQ-XXX para formalizar implementación
3. ⏭️ Prototipar Research Specialist custom agent (QUANT-001)

### Siguiente sesión
1. Validar prototipo Research Specialist
2. Convertir Repository Guardian (QUANT-002)
3. Probar handoff: research → guardian

### Próximas 2-3 sesiones
1. Completar conversión agentes core (QUANT-002)
2. Actualizar SUPER_AGENT orchestration (QUANT-003)
3. Integrar skills (QUANT-004)
4. Documentar arquitectura (QUANT-005)

---

## REFERENCIAS

### DeepWiki Research
- `microsoft/vscode` - runSubagent tool protocol
- `microsoft/vscode` - Custom agents (ICustomAgent, IChatModeService)

### SIA Framework Files
- `.github/copilot-instructions.md` - SUPER_AGENT identity
- `agents/research_specialist.md` - Research Specialist SPR
- `agents/repository_guardian.md` - Repository Guardian SPR
- `skills/create_expert_agent.md` - Agent creation methodology

### VS Code Documentation
- Chat Participants API
- Language Model API
- Custom Agents Configuration

---

**Document Version**: 1.0.0  
**Created**: 2025-11-30  
**Author**: SUPER_AGENT (First Principles Analysis)  
**Status**: ✅ Analysis Complete → Ready for REQ formalization
