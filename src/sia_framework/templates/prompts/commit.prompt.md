```prompt
---
name: commit
description: Genera commit(s) para los cambios de la sesión actual
argument-hint: "[opcional: archivos específicos o scope]"
---

**OBJETIVO:** Commitear SOLO los cambios relacionados con la sesión/QUANT actual.

---

**PROTOCOLO:**

1. **Identifica contexto de sesión:**
   - Lee el QUANT activo del REQ actual
   - Revisa `git status` para ver archivos modificados
   - Filtra SOLO archivos relacionados con el QUANT trabajado

2. **Clasifica los cambios:**
   - ✅ **INCLUIR**: Archivos del QUANT actual (código, tests, docs del REQ)
   - ❌ **EXCLUIR**: Cambios no relacionados (otros REQs, archivos random)
   - ⚠️ **PREGUNTAR**: Si hay duda sobre pertenencia

3. **Genera commit(s) atómicos:**
   - Un commit por unidad lógica de trabajo
   - Formato: `type(scope): descripción concisa`
   - Types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`

4. **Ejecuta:**
   - `git add <archivos-relevantes>`
   - `git commit -m "mensaje"`

---

**FORMATO DE COMMIT:**

```
type(scope): título corto (max 50 chars)

[QUANT-XXX-YYY]: Descripción breve

- Bullet 1: cambio específico
- Bullet 2: otro cambio
- ...

Files:
- path/to/file1.py
- path/to/file2.py
```

**TIPOS COMUNES:**
- `feat(domain)` - Nueva funcionalidad de dominio
- `feat(app)` - Use cases de aplicación
- `feat(infra)` - Infraestructura (repos, services)
- `feat(api)` - Endpoints API
- `test(unit)` - Tests unitarios
- `test(integration)` - Tests de integración
- `docs(req)` - Documentación de requirements
- `docs(prompts)` - Cambios en prompts SIA

---

**REGLAS ESTRICTAS:**

- ❌ **NUNCA** commitear archivos no relacionados con la sesión
- ❌ **NUNCA** mezclar cambios de múltiples QUANTs en un commit
- ❌ **NUNCA** commitear sin verificar `git status` primero
- ✅ **SIEMPRE** separar código de tests en commits diferentes (opcional)
- ✅ **SIEMPRE** incluir QUANT ID en el mensaje
- ✅ **PREGUNTAR** si hay archivos ambiguos

---

**EJEMPLOS:**

```bash
# Commit de feature
git commit -m "feat(infra): implement ConnectionManager for WebSocket sessions

QUANT-011-003: Infrastructure ConnectionManager

- Add ConnectionManager class with Dict[UUID, List[WebSocket]]
- Implement connect(), disconnect(), broadcast_to_transcription()
- 22 unit tests covering all acceptance criteria

Files:
- backend/src/minute_saas/infrastructure/websocket/connection_manager.py
- backend/tests/infrastructure/websocket/test_connection_manager.py"

# Commit de docs
git commit -m "docs(prompts): update activate.prompt.md to use slash commands

- Change @activate to /activate
- Standardize prompt references"
```

---

**USO:**

```
/commit                     # Commitea cambios de la sesión actual
/commit "solo tests"        # Commitea solo los tests
/commit --all               # Incluye TODOS los cambios (usar con cuidado)
```
```
