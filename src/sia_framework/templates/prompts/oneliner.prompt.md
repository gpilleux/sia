```prompt
---
name: oneliner
description: Genera ONE LINER activation command para siguiente tarea
argument-hint: "[opcional: REQ-ID o contexto]"
---

**OBJETIVO:** Devolver SOLO el one-liner de activación, listo para copiar.

**PROTOCOLO:**

1. Identifica siguiente QUANT pendiente:
   - Escanea `.sia/requirements/REQ-*/REQ-*_quant_breakdown.md`
   - Busca primer QUANT con estado `⏳` (pendiente)
   - O usa REQ-ID proporcionado por usuario

2. Extrae: REQ-ID, QUANT-ID, Título, Detalle técnico crítico

3. **OUTPUT OBLIGATORIO** (SOLO esto, nada más):

```
/activate + "Implementa REQ-{ID} QUANT-{N}: {Título} - {detalle técnico}"
```

**REGLAS ESTRICTAS:**
- ❌ NO explicaciones
- ❌ NO contexto adicional  
- ❌ NO bullets ni secciones
- ❌ NO "Aquí está el one-liner"
- ✅ SOLO el comando en code block para fácil copiado

**EJEMPLO DE OUTPUT CORRECTO:**

```
/activate + "Implementa REQ-011 QUANT-003: ConnectionManager - WebSocket Dict[UUID, List[WebSocket]]"
```
```
