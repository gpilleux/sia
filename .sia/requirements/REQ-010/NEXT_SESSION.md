# NEXT SESSION: Validación de /clean slash command

**TASK:** Probar `/clean` en escenario real del workspace SIA

---

## TEST PLAN

### Caso 1: Dry-Run (Default)
```
User: /clean
Expected: Análisis completo sin ejecutar movimientos
Validates:
- Detección de archivos fuera de lugar
- Clasificación automática (prompts, skills, docs, temporales)
- Output formateado con plan detallado
- NO ejecuta movimientos (solo análisis)
```

### Caso 2: Interactivo (Con Confirmación)
```
User: /clean
Agent: [Presenta plan]
User: @continue
Expected: Ejecuta movimientos aprobados + backup
Validates:
- Creación de backup en .sia/backup/{timestamp}/
- Movimientos ejecutados correctamente
- Log generado en .sia/metadata/cleanup_{timestamp}.log
- Archivos en ubicaciones canónicas
```

### Caso 3: Detección de Temporales
```
Setup: Crear .DS_Store, __pycache__/ en root
User: /clean
Expected: Detección y propuesta de eliminación
Validates:
- Lista de temporales detectados
- Propuesta de limpieza
- Ejecución segura (con confirmación)
```

### Caso 4: Safety Gates
```
Setup: Crear archivo en .git/, sia/
User: /clean --force
Expected: NUNCA tocar archivos protegidos
Validates:
- .git/ ignorado
- sia/* ignorado (READ-ONLY submodule)
- pyproject.toml ignorado
- .env ignorado
```

### Caso 5: Rollback
```
Setup: Ejecutar cleanup con movimientos
User: Revisar .sia/backup/{timestamp}/
Expected: Backup completo disponible
Validates:
- Estructura de backup correcta
- git checkout posible desde backup
- Log de movimientos completo
```

---

## HEURÍSTICAS DE CLASIFICACIÓN A VALIDAR

**Prompts:**
- Archivos con frontmatter YAML + `name:` → `.sia/prompts/`
- Detectar si es framework vs proyecto

**Skills:**
- Scripts ejecutables con shebang → `.sia/skills/`
- Archivos `.py` con imports de análisis

**Docs:**
- Markdown sin frontmatter → `docs/` o `.sia/knowledge/`
- Detectar si es knowledge (patterns, lessons) vs user-facing

**Temporales:**
- `.DS_Store`, `__pycache__`, `*.pyc`
- `htmlcov/`, `.pytest_cache/`
- Backups >30 días en `.sia/backup/`

---

## SUCCESS CRITERIA

- [ ] Dry-run funciona correctamente (análisis sin ejecución)
- [ ] Clasificación automática precisa (>90% casos)
- [ ] Confirmación obligatoria antes de mover
- [ ] Backup automático creado pre-ejecución
- [ ] Log completo de movimientos
- [ ] Safety gates respetados (NUNCA toca archivos críticos)
- [ ] Output claro y accionable

---

## ONE-LINER PARA PRÓXIMA SESIÓN

```
/activate + "Validar /clean command con test plan en REQ-010/NEXT_SESSION.md"
```
