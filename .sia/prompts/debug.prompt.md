---
name: debug
description: Análisis OMEGA CRITICAL por primeros principios
---

Analicemos esto OMEGA CRITICAL 🔍

---

**PROTOCOLO:**
1. **Primeros Principios** → Entender la raíz del problema
2. **Domain Research First** → Leer código existente antes de asumir
3. **Preguntas clave:**
   - ¿Cuál es el flujo esperado?
   - ¿Dónde se rompe?
   - ¿Qué asunciones son incorrectas?
4. **Patterns** → Revisión de patrones documentados de experiencias pasadas (`.sia/patterns`)

**MCP SOURCES:**
- `google/adk-python` → Si es problema ADK
- `idosal/mcp-ui` → Si es problema UIResource/rendering
- Playwright MCP → Si necesitas inspeccionar UI

**PRINCIPIOS:** DDD | SOLID | KISS para solución limpia

---

NO implementes solución hasta entender completamente el problema.
Guardian Enforcer activo para evitar parches.

---