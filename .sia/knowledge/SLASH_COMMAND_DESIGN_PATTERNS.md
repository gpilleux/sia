# Slash Command Design Patterns

**Meta-Knowledge**: Principios para crear comandos de calidad industrial

---

## ANATOMÍA DE UN SLASH COMMAND PERFECTO

### 1. FRONTMATTER (YAML)

```yaml
---
name: comando          # Nombre del comando (sin /, lowercase, snake_case si multi-palabra)
description: "Breve descripción de 1 línea (50-80 chars)"  # Qué hace, no cómo
argument-hint: "<tipo de input esperado>"  # Placeholder que ve el usuario al autocompletar
---
```

**Reglas:**
- `name`: Verbo de acción cuando posible (`activate`, `sync`, `debug`, `test`)
- `description`: Valor para el usuario, no tecnicismos ("Create requirement..." > "Execute pipeline...")
- `argument-hint`: Específico y útil (`"<requirement description>"` > `"<text>"`)

---

### 2. TÍTULO VISUAL

```markdown
🔥 **MAYÚSCULAS CON EMOJI**
```

**Propósito**: Impacto visual, energía, contexto inmediato

**Patrones observados:**
- 🚀 **QUANTUM ACTIVATION PROTOCOL** (activate)
- 📋 **AUTOMATED REQUIREMENT PIPELINE** (req)
- 🔄 **FRAMEWORK SYNC PROTOCOL** (sync)
- 🔍 **OMEGA CRITICAL** (debug)

**Principios:**
- Emoji relevante al dominio (🚀 activación, 📋 documentación, 🔄 sincronización)
- Mayúsculas para protocolo/sistema
- Máximo 4-5 palabras

---

### 3. ONE-LINER CONCEPTUAL

```markdown
Frase corta explicando transformación o propósito central.
```

**Ejemplos:**
- "Transforma input natural → REQ completo (Capture → Research → Reasoning → QUANT → Docs)."
- "Activa todos los super poderes del Super Agent para esta sesión."
- "Super Agent ejecuta sincronización usando **SOLO tools nativas**."

**Formato:**
- 1-2 líneas máximo
- Puede incluir flujo visual (`Input → Proceso → Output`)
- Enfatizar palabras clave con **bold**

---

### 4. PROTOCOLO (PASOS NUMERADOS)

```markdown
**PROTOCOLO:**
1. Paso 1 → Acción concreta
2. Paso 2 → Acción concreta
3. ...
```

**Anti-patrones detectados:**
- ❌ Demasiado detalle (el prompt NO es documentación técnica)
- ❌ Instrucciones imperativas ("Lee X, luego escribe Y") → Mejor: "Valida input → Si vago: preguntar"
- ❌ Lógica compleja con if/else anidados → Mejor: Heurísticas de alto nivel

**Patrón correcto:**
- Máximo 6-8 pasos de alto nivel
- Cada paso = 1 frase (puede tener sub-clarificación con →)
- Usa símbolos para brevedad (`→`, `⇒`, `∀`, `∃`)
- Si hay condicionales, usar formato compacto: "Si X → Y, sino Z"

**Ejemplo perfecto** (req.prompt.md):
```markdown
1. **Valida Input** → Si vago: preguntar (component, bounded context, success criteria)
2. **Si multi-context** → Sugerir split (REQ-{ID} por contexto)
3. **Auto-increment ID** → Scan `.sia/requirements/REQ-\d+`, max+1, format REQ-{ID:03d}
```

**Ejemplo deficiente** (inicial de req, 627 líneas):
```markdown
1. **Validar Input**
   - Leer input del usuario
   - Si input vago:
     - Preguntar por component
     - Preguntar por bounded context
     - Preguntar por success criteria
   - Si input claro:
     - Continuar
   - Si multi-context:
     - Explicar por qué debe split
     - Sugerir REQ-{ID} por cada contexto
```

---

### 5. FASES (Si aplica para comandos multi-etapa)

```markdown
**FASE 1: NOMBRE**
- Bullet point conciso
- Bullet point conciso
- Referencia a template si aplica

**FASE 2: NOMBRE**
...
```

**Reglas:**
- Solo si el comando tiene múltiples etapas claras
- Máximo 5-6 fases
- Cada fase: 3-5 bullets
- Bullets = Qué hacer, no paso a paso cómo

**Ejemplo perfecto** (req.prompt.md):
```markdown
**FASE 1: CAPTURE**
- Usa `sia/requirements/_templates/REQUIREMENT_TEMPLATE.md`
- Crea `.sia/requirements/REQ-{ID}/REQ-{ID}.md`
- Extrae: Problem, Value, Acceptance Criteria, Tech Context
- Aplica SPR compression (70-80% token reduction)
```

**Nota:** Comandos simples (activate, debug, test) NO necesitan fases, solo protocolo.

---

### 6. MCP SOURCES (MANDATORY)

```markdown
**MCP SOURCES (MANDATORY):**
- `mcp_tool_name` → Cuándo usar, qué repos
- Ejemplo de repos según contexto
```

**Propósito**: Documentar investigación obligatoria

**Patrones:**
- Listar tools MCP relevantes (DeepWiki, repo-indexer, Pylance)
- Especificar repos según contexto (condicional: "Si auth → `google/adk-python`")
- Marcar como MANDATORY si investigación es no-negociable

**Ejemplo:**
```markdown
**MCP SOURCES (MANDATORY):**
- `mcp_deepwiki_ask_question` → Research obligatorio (≥1 invocation)
- Repos según contexto: `google/adk-python`, `idosal/mcp-ui`, `fastapi/fastapi`
```

---

### 7. TEMPLATES (Si aplica)

```markdown
**TEMPLATES:**
- `ruta/relativa/al/template.md`
```

**Cuándo incluir:**
- Comandos que crean documentos formales (req, quant, handoff)
- Listar rutas relativas al workspace root (sia/)
- Solo templates USADOS por el comando, no todos los disponibles

---

### 8. PRINCIPIOS

```markdown
**PRINCIPIOS:**
- **Research First**: NUNCA asumir, siempre investigar
- **DDD | SOLID | KISS**: ...
- **Activation Gates**: ...
```

**Formato:**
- Bold para nombre del principio
- Colon (:) + descripción de 1 línea
- Máximo 4-6 principios (los más relevantes al comando)

**Principios universales** (incluir siempre que apliquen):
- Research First
- DDD | SOLID | KISS
- SPR Compression (si genera docs)
- Activation Gates (si requiere confirmación)
- Δ(Code) ⇒ Δ(Docs) (si modifica código)

---

### 9. ANTI-PATTERNS

```markdown
**ANTI-PATTERNS:**
- ❌ Descripción breve del error común
```

**Propósito**: Prevenir errores recurrentes

**Reglas:**
- Máximo 4-5 anti-patterns
- Usar emoji ❌ para visibilidad
- Frases cortas y específicas
- Basados en experiencia real (no teóricos)

**Ejemplo:**
```markdown
**ANTI-PATTERNS:**
- ❌ Skip MCP DeepWiki (Research First mandatory)
- ❌ Ejecutar sin presentar plan
- ❌ Crear NEXT_SESSION.md en ubicación incorrecta
```

---

### 10. OUTPUT FINAL

```markdown
**OUTPUT FINAL:**
```
Formato visual del resultado esperado
```
```

**Propósito**: Template del reporte que debe generar el agente

**Formato:**
- Usar bloque de código para estructura
- Emojis para secciones (✅, 📋, 🔬, 📊, 🎯)
- Variables en `{braces}` para valores dinámicos
- Incluir metadatos clave (archivos creados, métricas, next action)

**Ejemplo perfecto** (req.prompt.md):
```markdown
**OUTPUT FINAL:**
```
✅ REQ-{ID} CREATED: {Title}
📋 3 docs generados (REQ.md, domain_analysis.md, quant_breakdown.md)
📚 Research: {repos consultados}
🔬 Invariants: {count} extraídos (notación matemática)
📊 QUANT: {N} tasks, {AI_h}h AI / {Human_h}h Human
🎯 NEXT: /activate + "Implementar REQ-{ID} QUANT-001"
```
```

---

### 11. METADATA ADICIONAL (Opcional)

```markdown
**LOCATION**: Ruta donde se generan archivos
**WORKFLOW REF**: Documento de referencia
**GUARDIAN**: Estado (Activo/Inactivo)
```

**Cuándo incluir:**
- Comandos que modifican estructura de archivos (req, quant, sync)
- Solo si aporta valor (no por completitud)

---

## CRITERIOS DE CALIDAD

### Extensión Target

**Rango ideal:** 25-50 líneas (sin contar frontmatter)

**Distribución observada:**
- `activate.prompt.md`: 34 líneas ✅
- `quant.prompt.md`: 23 líneas ✅
- `debug.prompt.md`: 21 líneas ✅
- `test.prompt.md`: 20 líneas ✅
- `req.prompt.md`: 94 líneas ⚠️ (límite aceptable para comando complejo)
- `sync.prompt.md`: 377 líneas ❌ (outlier, documentación técnica embebida)

**Regla de oro:**
- Comandos simples (activate, debug, test): 20-30 líneas
- Comandos complejos (req, quant, handoff): 50-100 líneas
- Comandos técnicos multi-fase (sync): 100-400 líneas (excepcional)

### Densidad de Información

**Objetivo:** Máxima información, mínimo token count

**Técnicas de compresión:**
1. **Símbolos sobre palabras**: `→` en vez de "y luego", `⇒` en vez de "implica"
2. **Bullets sobre párrafos**: Lista de 3 items < párrafo de 3 oraciones
3. **Referencias sobre explicaciones**: "Usa template X" < copiar estructura del template
4. **Notación matemática**: `∀x ∈ Set` < "para todos los elementos x en el conjunto Set"
5. **Paréntesis para contexto**: "Auto-increment (max+1)" < "Buscar el máximo y sumarle 1"

**Ejemplo de compresión extrema:**
```markdown
# Antes (verbose)
Si el usuario proporciona un input vago que no permite identificar claramente el componente, 
el bounded context o los criterios de aceptación, el agente debe hacer preguntas para clarificar.

# Después (comprimido)
Si vago → preguntar (component, bounded context, success criteria)
```

### Legibilidad Visual

**Jerarquía clara:**
- H1 (`#`) = NUNCA (frontmatter es título)
- H2 (`##`) = NUNCA (prompts no necesitan sections)
- Bold mayúsculas = Secciones principales (`**PROTOCOLO:**`)
- Bold mixtas = Sub-secciones (`**FASE 1: CAPTURE**`)
- Bullets = Items de lista
- Código inline = Rutas, comandos, variables (`REQ-{ID}`)

**Whitespace estratégico:**
- Línea en blanco entre secciones principales
- NO línea en blanco entre bullets de misma lista
- Línea horizontal (`---`) para separación visual fuerte (máximo 2-3 por prompt)

---

## PATRONES DE LENGUAJE

### Imperativo vs Declarativo

**❌ Imperativo** (no usar):
```markdown
Lee el archivo X
Luego escribe el archivo Y
Después ejecuta Z
```

**✅ Declarativo** (usar):
```markdown
Archivo X → Procesamiento → Archivo Y
Z ejecutado post-validación
```

**Razón:** Los prompts NO son scripts paso a paso, son contexto para razonamiento.

### Condicionales Compactos

**❌ Verboso:**
```markdown
Si el usuario proporciona input claro:
  Continuar con el flujo normal
Si el usuario proporciona input vago:
  Hacer preguntas de clarificación
Si el usuario proporciona múltiples contextos:
  Sugerir dividir en múltiples REQs
```

**✅ Compacto:**
```markdown
Input claro → Continuar | Vago → Preguntar | Multi-context → Sugerir split
```

O con bullets si hay más detalle:
```markdown
- Si vago → Preguntar (component, bounded context, success criteria)
- Si multi-context → Sugerir split (REQ-{ID} por contexto)
```

### Ejemplos Inline vs Bloques

**Inline** (para valores simples):
```markdown
Format: REQ-{ID:03d} (ejemplo: REQ-001, REQ-042)
```

**Bloques** (para estructura completa):
```markdown
**OUTPUT FINAL:**
```
✅ REQ-{ID} CREATED: {Title}
📋 Docs: REQ.md, domain_analysis.md
```
```

---

## CHECKLIST DE VALIDACIÓN

Antes de considerar un slash command "listo para producción":

### Estructura
- [ ] Frontmatter YAML válido (name, description, argument-hint)
- [ ] Título visual con emoji y mayúsculas
- [ ] One-liner conceptual (1-2 líneas)
- [ ] Protocolo o fases claramente definidos
- [ ] Sección de principios (Research First, DDD, etc.)
- [ ] Anti-patterns documentados (≥3 items)
- [ ] Output final con template visual

### Contenido
- [ ] MCP sources especificados (si aplica investigación)
- [ ] Templates listados (si aplica generación de docs)
- [ ] Extensión adecuada (20-100 líneas, justificar si >100)
- [ ] Símbolos usados para brevedad (`→`, `⇒`, `∀`)
- [ ] Referencias a framework, no explicaciones largas

### Calidad
- [ ] Zero instrucciones imperativas tipo "Lee X, luego Y"
- [ ] Condicionales compactos (inline o bullets, no párrafos)
- [ ] Ejemplos solo si aportan valor crítico
- [ ] Metadatos relevantes (LOCATION, WORKFLOW REF si aplica)
- [ ] Validation gates explícitos (HALT, espera confirmación)

### Integración
- [ ] Archivo creado en `sia/templates/prompts/`
- [ ] Archivo sincronizado en `.sia/prompts/`
- [ ] Entrada agregada en `docs/SLASH_COMMANDS.md` (Quick Reference + Detailed)
- [ ] NEXT_SESSION.md creado para testing (si es nuevo comando)

---

## ANTI-PATTERNS GLOBALES

### ❌ Documentación Técnica Embebida

**Problema:** Confundir el prompt con un manual de usuario

**Ejemplo deficiente:**
```markdown
## FASE 3: SINCRONIZACIÓN INTELIGENTE

### 3.1 Nuevos Prompts (NO existen localmente)

For each file in new_prompts:
  
  Step 1: Copiar archivo directamente
  Tool: run_in_terminal(
    command: f"cp sia/templates/prompts/{filename} .sia/prompts/{filename}",
    explanation: f"Copiar {filename} a prompts locales"
  )
  
  Step 2: Calcular hash
  Tool: run_in_terminal(...)
  ...
```

**Por qué falla:** 
- Exceso de detalle técnico (377 líneas)
- Pseudo-código imperativo
- Debería estar en README.md de skills/, no en prompt

**Solución:**
- Prompts = Contexto y heurísticas (50 líneas)
- README.md = Documentación detallada (sin límite)

### ❌ Ejemplos Innecesarios

**Problema:** Incluir ejemplos cuando el pattern es obvio

**Ejemplo deficiente:**
```markdown
Format: REQ-{ID:03d}

Ejemplos:
- REQ-001
- REQ-002
- REQ-042
- REQ-137
```

**Solución:**
```markdown
Format: REQ-{ID:03d} (ejemplo: REQ-001)
```

### ❌ Lógica Duplicada

**Problema:** Especificar lo mismo en múltiples secciones

**Ejemplo:**
```markdown
**PROTOCOLO:**
1. Validar input → Si vago: preguntar

**FASE 1:**
- Si input vago, preguntar por detalles

**ANTI-PATTERNS:**
- ❌ No validar input vago
```

**Solución:** Una sola mención en la sección más relevante (PROTOCOLO).

### ❌ Scope Creep

**Problema:** Incluir capacidades no relacionadas al comando

**Ejemplo:** Un prompt `/req` que también explica cómo sincronizar framework, hacer rollback, etc.

**Solución:** Un comando = Una responsabilidad. Si necesita explicación extensa → Separar en comando distinto.

---

## PROCESO DE CREACIÓN (Meta-Workflow)

### Paso 1: Research

```markdown
**Antes de escribir una línea:**
1. Leer 3-5 prompts existentes (patrones de estructura)
2. MCP DeepWiki → `microsoft/vscode` (Chat Prompts API)
3. MCP DeepWiki → `google/adk-python` (reasoning patterns si aplica)
4. Identificar comandos similares (reutilizar patrones)
```

### Paso 2: Domain Analysis

```markdown
**Preguntas clave:**
- ¿Qué transformación realiza el comando? (Input → Output)
- ¿Qué investigación requiere? (MCP sources)
- ¿Genera documentos? (Templates necesarios)
- ¿Es multi-fase o single-step?
- ¿Requiere confirmación del usuario? (Activation gates)
```

### Paso 3: Diseño SPR

```markdown
**Drafting comprimido:**
1. Escribir versión larga (ignorar límites)
2. Aplicar técnicas de compresión:
   - Párrafos → Bullets
   - Bullets → Inline con símbolos
   - Explicaciones → Referencias
   - Ejemplos → Solo el crítico
3. Target: Reducir 70-80% de tokens iniciales
4. Validar legibilidad (no sacrificar claridad)
```

### Paso 4: Validación

```markdown
**Checklist:**
- [ ] Extensión adecuada (20-100 líneas)
- [ ] Estructura completa (frontmatter → output)
- [ ] Zero imperatives ("Lee X, luego Y" → "X → Procesamiento → Y")
- [ ] MCP sources documentados
- [ ] Principios y anti-patterns incluidos
```

### Paso 5: Integración

```markdown
**Deliverables:**
1. `sia/templates/prompts/{comando}.prompt.md` (source of truth)
2. `.sia/prompts/{comando}.prompt.md` (instalado)
3. `docs/SLASH_COMMANDS.md` actualizado (Quick Ref + Detailed)
4. `.sia/requirements/REQ-XXX/NEXT_SESSION.md` con testing plan
```

---

## EJEMPLOS DE REFERENCIA

### Comando Simple (20-30 líneas)

**`test.prompt.md`** - Ejemplo perfecto de brevedad con impacto:
```markdown
---
name: test
description: Generar tests con Domain Research First obligatorio
---

Momentum perfecto para tests! 🧪

**PROTOCOLO (MANDATORY):**
1. **Domain Research First** → LEE la entidad/servicio ANTES
2. Tests validan **invariantes**, NO implementación
3. Usa MCP DeepWiki para best practices

**MCP SOURCES:**
- `google/adk-python` → Patterns testing ADK
- Código existente en `backend/tests/`

**PRINCIPIOS:**
- DDD → Tests reflejan lenguaje ubicuo
- SOLID → Tests responsabilidad única
- KISS → Tests simples y directos

NUNCA escribas tests sin leer primero el código.
Guardian Enforcer valida cobertura edge cases.
```

**Por qué es perfecto:**
- 20 líneas totales
- Protocolo ultra-compacto (3 pasos)
- Principios esenciales (DDD, SOLID, KISS)
- MCP sources específicos
- Anti-pattern implícito en última línea

### Comando Complejo (50-100 líneas)

**`req.prompt.md`** - Ejemplo de complejidad manejada:
- 94 líneas (límite superior aceptable)
- 6 pasos de protocolo (validaciones pre-ejecución)
- 5 fases claras (Capture, Research, Reasoning, QUANT, Docs)
- MCP sources condicionales (según contexto)
- Output template visual completo

**Por qué funciona:**
- Compresión extrema aplicada (627 líneas iniciales → 94 finales, 85% reducción)
- Cada fase = 4-5 bullets (no más)
- Referencias a templates, no duplicación de contenido
- Heurísticas de razonamiento automatizado (compactas)

### Comando Técnico (100-400 líneas)

**`sync.prompt.md`** - Outlier aceptable:
- 377 líneas (excepcional, no norma)
- Razón: Lógica de sincronización compleja con edge cases críticos
- Estructura: 6 fases + 4 edge cases + 3 variantes de comando
- Formato: Pseudo-código instructivo (tool-based execution)

**Lección aprendida:**
- Comandos de "orquestación técnica" pueden ser largos
- Pero MAYORÍA de comandos deben ser 20-50 líneas
- Si supera 100 líneas → Cuestionar si debería ser skill/script externo

---

## EVOLUCIÓN Y MANTENIMIENTO

### Cuándo Refactorizar

**Triggers:**
- Feedback de usuario: "El comando no hace lo que esperaba"
- Bugs recurrentes: Mismo error en múltiples sesiones
- Complejidad creciente: Prompt supera 150 líneas sin justificación
- Scope creep: Comando hace 3+ cosas no relacionadas

### Proceso de Refactor

```markdown
1. **Audit**: Leer prompt actual con ojos críticos
2. **Compress**: Aplicar técnicas de SPR (símbolos, bullets, referencias)
3. **Split**: Si hace >1 cosa, dividir en comandos separados
4. **Test**: Validar con casos de uso reales
5. **Document**: Actualizar SLASH_COMMANDS.md y copilot-instructions.md
```

### Versionado

**Pattern:**
- Cambios menores (typos, clarificaciones): No requiere versión
- Cambios de comportamiento (nuevas fases, MCP sources): Documentar en CHANGELOG.md
- Breaking changes (cambio de formato output): Crear migración y documentar en REQ-XXX

---

## REFERENCIAS

**Documentación oficial:**
- VS Code Chat Prompts API: `microsoft/vscode` (via MCP DeepWiki)
- ADK Reasoning Patterns: `google/adk-python` (via MCP DeepWiki)

**Archivos del framework:**
- `sia/templates/prompts/` - Source of truth de todos los comandos
- `docs/SLASH_COMMANDS.md` - Documentación de usuario
- `.sia/prompts/` - Comandos instalados en proyecto

**Meta-knowledge:**
- `sia/core/CONCEPTS.md` - SPR compression, Stack phases
- `sia/core/SUPER_AGENT.md` - Principios de diseño del framework
- `.sia/knowledge/SLASH_COMMAND_DESIGN_PATTERNS.md` - Este documento

---

**VERSION**: 1.0.0  
**CREATED**: 2025-11-30  
**SOURCE**: Análisis post-implementación REQ-009 (req.prompt.md)  
**LESSONS**: 627 líneas iniciales → 94 finales (85% compresión), validación de patterns existentes

**STATUS**: ✅ Knowledge base activa para futuras creaciones de slash commands
