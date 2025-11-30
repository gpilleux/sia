---
name: test
description: Generar tests con Domain Research First obligatorio
---

Momentum perfecto para tests! 🧪

---

**PROTOCOLO (MANDATORY):**
1. **First Principles**: Tests validan AXIOMAS, no implementación
   - ❌ "Test that method X calls method Y" (implementation detail)
   - ✅ "Test that invariant holds: ∀ user: user.age >= 18" (axiom)
   - Black box: Input → Expected Output (refactoring safe)
   
2. **Domain Research First** → LEE la entidad/servicio ANTES de escribir tests
   - Identifica axiomas del dominio (qué verdades fundamentales protege)
   - Ejemplo: "Email must be valid" → axiom: ∀ email: regex_match(email)
   
3. Tests validan **invariantes de dominio** (derivados de axiomas), NO detalles de implementación

4. Usa MCP DeepWiki para mejores prácticas de testing

5. **Coverage = Axioms Tested** (no line coverage)
   - 100% de axiomas cubiertos > 100% de líneas
   - Axiom no cubierto = potential bug

**MCP SOURCES:**
- `google/adk-python` → Patterns de testing ADK
- Código existente en `backend/tests/`

**PRINCIPIOS:**
- DDD → Tests reflejan lenguaje ubicuo
- SOLID → Tests con responsabilidad única
- KISS → Tests simples y directos

---

NUNCA escribas tests sin leer primero el código que vas a testear.
Guardian Enforcer valida cobertura de casos edge.
