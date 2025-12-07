```prompt
---
name: oneliner
description: Genera ONE LINER para siguiente tarea en workflow de requirements
argument-hint: "[opcional: REQ-ID o contexto]"
---

🎯 **NEXT TASK ONE LINER**

Genera one-liner para siguiente tarea en workflow de requirements (contexto ya documentado en breakdown).

---

**PROTOCOLO:**

1. **Identifica siguiente tarea**:
   - Lee `NEXT_SESSION.md` si existe
   - O escanea `.sia/requirements/REQ-*/` para próximo QUANT pendiente
   - O usa contexto proporcionado por usuario

2. **Extrae información mínima crítica**:
   - REQ-ID + QUANT-ID
   - Título de la tarea (del breakdown)
   - UN detalle crítico específico (bounded context, constraint, o técnica)

3. **Sintetiza ONE LINER**:
   - Formato: `"Implementa REQ-XYZ QUANT-N: [título] [detalle crítico]"`
   - Máximo 1 oración
   - Super Agent hará la investigación profunda

**ESTRUCTURA:**
```
Implementa REQ-{ID} QUANT-{N}: {Título} {detalle mínimo crítico}
```

**EJEMPLOS:**
✅ "Implementa REQ-003 QUANT-001: OAuth Provider Configuration usando Google ADK patterns"
✅ "Implementa REQ-007 QUANT-003: Message Entity Validation con ValueObjects RFC 5322"
✅ "Implementa REQ-012 QUANT-002: AsyncRepository Pattern respetando dependency inversion"

**NO incluir:**
❌ Descripción completa (ya está en breakdown)
❌ Todos los acceptance criteria (Super Agent los lee)
❌ Investigación previa (Super Agent la ejecuta)

---

**CONTEXT SOURCES:**
- `.sia/requirements/REQ-*/NEXT_SESSION.md`
- `.sia/requirements/REQ-*/REQ-*_quant_breakdown.md`
- Argument hint del usuario

**OUTPUT FORMAT:**
```
📌 NEXT TASK:
Implementa REQ-{ID} QUANT-{N}: {Título} {detalle crítico}

📂 CONTEXT:
- .sia/requirements/REQ-{ID}/REQ-{ID}_quant_breakdown.md
- .sia/requirements/REQ-{ID}/REQ-{ID}_domain_analysis.md
```

🎯 **ACTIVACIÓN:**
```
/activate "Implementa REQ-{ID} QUANT-{N}: {título breve}"
```

**PRINCIPIOS:** Mínimo contexto | Referencia a docs | Super Agent investiga

```
