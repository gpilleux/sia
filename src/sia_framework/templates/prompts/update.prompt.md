---
name: update
description: Actualizar documentación del REQ activo con SPR compression
---

Excelente trabajo, bravo!! 📝 Documentemos los avances.

---

**PROTOCOLO:**
1. Actualiza documentación del REQ activo en `.sia/requirements/REQ-*/`
2. **SPR Compression** → Máxima densidad, mínima extensión
3. Si es grande → Insertar por partes (iterativo)

**DESTINOS:**
- QUANT completions → `.sia/requirements/REQ-*/QUANT_*_COMPLETION.md`
- Progress → `REQ-*_quant_breakdown.md`
- Next session → `NEXT_SESSION.md`

**PRINCIPIOS:** DDD | SOLID | KISS | CLEAN CODE
**INVARIANTE:** `Δ(Code) ⇒ Δ(Docs)` - Code y docs son atómicos

---

Usar MCP DeepWiki si necesitas validar mejores prácticas de documentación.
