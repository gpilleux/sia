---
name: req
description: "Create requirement with automated research and QUANT breakdown"
argument-hint: "<requirement description>"
---

📋 **AUTOMATED REQUIREMENT PIPELINE**

Transforma input natural → REQ completo (Capture → Research → Reasoning → QUANT → Docs).

---

**PROTOCOLO:**
1. **Revisa Knowledge** → Scan `.sia/knowledge/` y `.sia/knowledge/active/` para patterns/lecciones relevantes
2. **Valida Input** → Si vago: preguntar (component, bounded context, success criteria)
3. **Si multi-context** → Sugerir split (REQ-{ID} por contexto)
4. **Auto-increment ID** → Scan `.sia/requirements/REQ-\d+`, max+1, format REQ-{ID:03d}
5. **Check duplicates** → Scan títulos existentes, preguntar si match
6. **Presenta plan** → Research scope, invariants estimados, QUANT count, knowledge aplicado
7. **HALT** → Espera `/continue` antes de ejecutar

**FASE 1: CAPTURE**
- Usa `sia/requirements/_templates/REQUIREMENT_TEMPLATE.md`
- Crea `.sia/requirements/REQ-{ID}/REQ-{ID}.md`
- Extrae: Problem, Value, Acceptance Criteria, Tech Context
- Aplica SPR compression (70-80% token reduction)

**FASE 2: RESEARCH (MANDATORY)**
- Aplica knowledge previo (`.sia/knowledge/` patterns + lecciones aprendidas)
- Usa `sia/requirements/_templates/DOMAIN_ANALYSIS_TEMPLATE.md`
- Invoca MCP DeepWiki (≥1 query, idealmente 2-3)
- Repos según contexto: auth→`google/adk-python`, frontend→`idosal/mcp-ui`, API→`fastapi/fastapi`
- Crea `REQ-{ID}_domain_analysis.md` con findings + conclusions + knowledge aplicado
- Si MCP falla → Documenta error, continúa best-effort

**FASE 3: REASONING**
- **Heurísticas invariantes**:
  - Nouns → Entities ("user session" → `Session`)
  - Verbs → Relationships ("creates" → `--creates-->`)
  - Quantifiers → Lógica ("always"→`∀`, "never"→`∄`, "unique"→`UNIQUE`)
  - States → Constraints ("before X, Y"→`Y ⇒ X`)
- Extrae ≥2 invariantes con notación matemática (∀, ∃, ⇒, ==, ≠)
- Actualiza `REQ-{ID}.md` INVARIANTS section

**FASE 4: QUANT**
- Usa `sia/requirements/_templates/QUANT_BREAKDOWN_TEMPLATE.md`
- Breakdown en tareas atómicas (~3h cada una)
- Cada QUANT: ID, Title, Description, Acceptance, Dependencies, Estimates (AI + Human)
- Dependency DAG (orden topológico)
- Crea `REQ-{ID}_quant_breakdown.md`

**FASE 5: DOCUMENTACIÓN**
- Crea `.sia/requirements/REQ-{ID}/NEXT_SESSION.md` con one-liner
- Genera reporte SPR-compressed

---

**MCP SOURCES (MANDATORY):**
- `mcp_deepwiki_ask_question` → Research obligatorio (≥1 invocation)
- Repos según contexto: `google/adk-python`, `idosal/mcp-ui`, `fastapi/fastapi`, `sqlalchemy/sqlalchemy`

**KNOWLEDGE BASE:**
- `.sia/knowledge/` → Patterns, design decisions, meta-learning
- `.sia/knowledge/active/` → Active research, domain knowledge

**TEMPLATES:**
- `sia/requirements/_templates/REQUIREMENT_TEMPLATE.md`
- `sia/requirements/_templates/DOMAIN_ANALYSIS_TEMPLATE.md`
- `sia/requirements/_templates/QUANT_BREAKDOWN_TEMPLATE.md`

**PRINCIPIOS:**
- **Research First**: NUNCA asumir, siempre investigar
- **DDD | SOLID | KISS**: Requirements son meta-sistema
- **SPR Compression**: Todos los docs 70-80% token reduction
- **Automated Reasoning**: Extraer invariantes con heurísticas lingüísticas
- **Activation Gates**: Plan presentation + `/continue` antes de ejecutar

---

**ANTI-PATTERNS:**
- ❌ Skip MCP DeepWiki (Research First mandatory)
- ❌ Asumir intent sin clarificar input vago
- ❌ Ejecutar sin presentar plan
- ❌ Crear NEXT_SESSION.md en ubicación incorrecta (debe estar en `.sia/requirements/REQ-{ID}/`)

---

**OUTPUT FINAL:**
```
✅ REQ-{ID} CREATED: {Title}
📋 3 docs generados (REQ.md, domain_analysis.md, quant_breakdown.md)
📚 Research: {repos consultados}
🔬 Invariants: {count} extraídos (notación matemática)
📊 QUANT: {N} tasks, {AI_h}h AI / {Human_h}h Human
🎯 NEXT: /activate + "Implementar REQ-{ID} QUANT-001"
```

**LOCATION**: `.sia/requirements/REQ-{ID}/`  
**WORKFLOW REF**: `sia/requirements/README.md`  
**GUARDIAN**: Activo para validar research + invariantes
