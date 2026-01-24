```prompt
---
name: clean
description: Organizar workspace - Archivos en ubicaciones canónicas
argument-hint: "[--dry-run|--force]"
---

🧹 **REPOSITORY CLEANUP PROTOCOL**

Organiza workspace → Archivos en ubicaciones correctas → Metadata sincronizada.

---

**PROTOCOLO:**
1. **Scan workspace** → Detectar archivos fuera de ubicaciones canónicas
2. **Clasificar** → Prompts, skills, requirements, docs, configs
3. **Proponer movimientos** → Mostrar plan, esperar confirmación (`@continue`)
4. **Ejecutar (si aprobado)** → Mover archivos, actualizar metadata
5. **Validar** → Verificar integridad post-cleanup

---

**DETECCIÓN AUTOMÁTICA:**
- `*.prompt.md` fuera de `.sia/prompts/` o `sia/templates/prompts/` → Clasificar (framework vs proyecto)
- Scripts Python en root → Clasificar (skill vs tool vs installer)
- Docs sueltos (`.md` en root/subdirs) → Consolidar en `docs/` o `.sia/knowledge/`
- Temporales → Limpiar (`.DS_Store`, `__pycache__`, `*.pyc`, `htmlcov/`, `.pytest_cache/`)
- Backups antiguos → Revisar `.sia/backup/` (mantener último mes)

**UBICACIONES CANÓNICAS:**
```
.sia/
  prompts/           → Proyecto-specific slash commands
  skills/            → Proyecto-specific análisis
  knowledge/         → Domain patterns, lessons learned
  requirements/      → REQ-XXX folders
  agents/            → Proyecto SPR
  metadata/          → Version, sync, hashes

sia/                 → Framework submodule (READ-ONLY)
  templates/prompts/ → Framework slash commands
  skills/            → Framework tools
  agents/            → Framework agents
  
docs/                → User-facing docs
tests/               → Test suite
```

**CLASIFICACIÓN HEURÍSTICA:**
- Contiene frontmatter YAML + `name:` → Prompt
- Ejecutable con shebang/imports → Skill/Script
- Tiene `## REQ-` header → Requirement doc
- Markdown general → Doc/Knowledge
- `.py` sin tests → Posible skill
- `test_*.py` → Test

---

**MODOS DE OPERACIÓN:**

**Dry-Run (default):**
```
/clean
/clean --dry-run
```
→ Escanea, clasifica, muestra plan, NO ejecuta

**Interactivo:**
```
/clean + [presentar plan]
User: @continue
```
→ Ejecuta movimientos aprobados

**Force (requiere confirmación explícita):**
```
/clean --force
```
→ Muestra plan, pide confirmación doble, ejecuta TODO

---

**SAFETY GATES:**
- **NUNCA** mover sin backup previo
- **NUNCA** tocar `.git/`, `pyproject.toml`, `package.json`, `.env`
- **NUNCA** borrar archivos del framework (`sia/*`)
- **NUNCA** modificar `.sia.detected.yaml`
- **PREGUNTA** antes de consolidar docs (puede haber WIP)
- **BACKUP** automático en `.sia/backup/{timestamp}/` antes de mover

---

**PRINCIPIOS:**
- **Safety First**: Dry-run por defecto, confirmación obligatoria
- **Traceability**: Log en `.sia/metadata/cleanup_{timestamp}.log`
- **Rollback**: Backup automático pre-ejecución
- **DDD**: Respeta bounded contexts (`.sia/` = proyecto, `sia/` = framework)
- **KISS**: Clasificación simple basada en heurísticas

---

**ANTI-PATTERNS:**
- ❌ Mover archivos sin confirmación
- ❌ Borrar sin backup
- ❌ Modificar archivos críticos (configs, .git)
- ❌ Asumir clasificación sin revisar contenido
- ❌ Ejecutar --force sin entender impacto

---

**OUTPUT FINAL:**
```
🧹 CLEANUP ANALYSIS

📁 ARCHIVOS DETECTADOS FUERA DE LUGAR:
   - test_script.py (root) → .sia/skills/
   - old_prompt.md (docs/) → .sia/prompts/
   - analysis.md (root) → .sia/knowledge/

🗑️  TEMPORALES DETECTADOS:
   - .DS_Store (12 archivos)
   - __pycache__/ (5 directorios)
   - htmlcov/ (1 directorio)

📊 RESUMEN:
   - Archivos a mover: 3
   - Temporales a eliminar: 18
   - Backups antiguos: 2 (>30 días)

🎯 ACCIÓN REQUERIDA:
   - Dry-run completado
   - Revisar plan arriba
   - Si apruebas: @continue
   - Si rechazas: Ignorar o especifica qué ajustar
```

---

**METADATA TRACKING:**
- `.sia/metadata/cleanup_{timestamp}.log` → Historial completo
- Formato: `YYYY-MM-DD HH:MM:SS | MOVED | src/path → dst/path`
- Rollback: `git checkout .sia/backup/{timestamp}/`

---

**WORKFLOW REF:** REQ-010 (Streamlined slash command creation)
**GUARDIAN:** Inactivo (workspace hygiene, no código)
```
