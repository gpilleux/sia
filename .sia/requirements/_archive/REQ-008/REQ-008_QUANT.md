# REQ-008 QUANT Breakdown - Smart Update System

**Parent**: REQ-008  
**Created**: 2025-11-29  
**Status**: 🔄 Active

---

## QUANT TASKS

### QUANT-008-001: Version Detection System
**Estimate**: 2h  
**Phase**: 1 - Core Update Logic  
**Priority**: High

**Specification**:
Implementar sistema de detección de versiones entre submódulo y proyecto.

**Acceptance Criteria**:
- ✅ Leer `sia/VERSION` (submódulo)
- ✅ Leer `.sia/VERSION` (proyecto)
- ✅ Comparar versiones (semantic versioning)
- ✅ Return boolean: `update_available`

**Files**:
- `installer/smart_update.py` (create)
- `.sia/VERSION` (create if missing)

**Dependencies**: None

**Test**:
```python
# sia/VERSION = 1.2.0
# .sia/VERSION = 1.0.0
# Expected: update_available = True
```

---

### QUANT-008-002: Template Diff Detection
**Estimate**: 2h  
**Phase**: 1 - Core Update Logic  
**Priority**: High

**Specification**:
Detectar diferencias entre `templates/` (submódulo) y `.sia/` (proyecto).

**Acceptance Criteria**:
- ✅ Scan all files in `sia/templates/`
- ✅ Compare with `.sia/` equivalent paths
- ✅ Classify: NEW, MODIFIED, DELETED, UNCHANGED
- ✅ Return diff report (dict structure)

**Files**:
- `installer/smart_update.py`

**Dependencies**: QUANT-008-001

**Test**:
```python
# NEW: sia/templates/prompts/x.md exists, .sia/prompts/x.md missing
# MODIFIED: both exist, hashes differ
# DELETED: .sia/prompts/y.md exists, sia/templates/prompts/y.md missing
```

---

### QUANT-008-003: Simple Copy Strategy
**Estimate**: 1h  
**Phase**: 1 - Core Update Logic  
**Priority**: High

**Specification**:
Implementar copia simple para archivos NUEVOS.

**Acceptance Criteria**:
- ✅ Copiar archivos clasificados como NEW
- ✅ Preservar estructura de directorios
- ✅ Log cada copia en stdout
- ✅ No sobrescribir archivos existentes

**Files**:
- `installer/smart_update.py`

**Dependencies**: QUANT-008-002

**Test**:
```bash
# sia/templates/prompts/new.prompt.md → .sia/prompts/new.prompt.md
# Expected: File copied, log message printed
```

---

### QUANT-008-004: Sync Log Generation
**Estimate**: 1h  
**Phase**: 1 - Core Update Logic  
**Priority**: Medium

**Specification**:
Generar `.sia/SYNC_LOG.md` con historial de cambios aplicados.

**Acceptance Criteria**:
- ✅ Timestamp de sincronización
- ✅ Lista de archivos copiados/modificados
- ✅ Versión anterior → versión nueva
- ✅ Append mode (mantener historial)

**Files**:
- `.sia/SYNC_LOG.md` (create/append)
- `installer/smart_update.py`

**Dependencies**: QUANT-008-003

**Test**:
```markdown
# Expected content:
## 2025-11-29 10:30:00
Version: 1.0.0 → 1.2.0
Files Updated:
- NEW: .sia/prompts/test.prompt.md
```

---

### QUANT-008-005: Hash-Based Change Detection
**Estimate**: 2h  
**Phase**: 2 - Merge Inteligente  
**Priority**: High

**Specification**:
Implementar detección de cambios locales usando SHA256 hashes.

**Acceptance Criteria**:
- ✅ Calcular hash de archivo en templates/
- ✅ Calcular hash de archivo en .sia/
- ✅ Si hashes difieren → MODIFIED
- ✅ Store original hash en `.sia/.hashes.json` (tracking)

**Files**:
- `installer/smart_update.py`
- `.sia/.hashes.json` (create)

**Dependencies**: QUANT-008-002

**Test**:
```python
# Template hash: abc123
# Local file hash: abc123 → Unchanged
# Local file hash: def456 → Modified locally
```

---

### QUANT-008-006: Backup System
**Estimate**: 2h  
**Phase**: 2 - Merge Inteligente  
**Priority**: High

**Specification**:
Crear sistema de backups automáticos antes de sobrescribir.

**Acceptance Criteria**:
- ✅ Crear directorio `.sia/.backups/`
- ✅ Copiar archivo a `.backups/{timestamp}_{filename}`
- ✅ Solo backup si archivo se va a sobrescribir
- ✅ Límite de 10 backups por archivo (FIFO cleanup)

**Files**:
- `installer/smart_update.py`
- `.sia/.backups/` (directory)

**Dependencies**: QUANT-008-005

**Test**:
```bash
# Sobrescribir .sia/prompts/x.md
# Expected: .sia/.backups/2025-11-29_10-30-00_x.md created
```

---

### QUANT-008-007: Conflict Detection & Reporting
**Estimate**: 2h  
**Phase**: 2 - Merge Inteligente  
**Priority**: High

**Specification**:
Detectar conflictos (archivo modificado local Y en template) y reportar.

**Acceptance Criteria**:
- ✅ Si archivo modificado localmente Y en template → CONFLICT
- ✅ Agregar entrada en SYNC_LOG.md: "⚠️ CONFLICT: {file}"
- ✅ No sobrescribir automáticamente
- ✅ Sugerir resolución manual

**Files**:
- `installer/smart_update.py`
- `.sia/SYNC_LOG.md`

**Dependencies**: QUANT-008-005, QUANT-008-006

**Test**:
```markdown
# SYNC_LOG.md expected:
⚠️ CONFLICT: .sia/prompts/activate.prompt.md
  - Local version modified
  - Template version modified
  - Action: Manual merge required
  - Backup: .backups/2025-11-29_10-30-00_activate.prompt.md
```

---

### QUANT-008-008: Dry-Run Mode
**Estimate**: 1h  
**Phase**: 2 - Merge Inteligente  
**Priority**: Medium

**Specification**:
Implementar modo `--dry-run` que simula cambios sin aplicar.

**Acceptance Criteria**:
- ✅ CLI flag: `python smart_update.py --dry-run`
- ✅ Mostrar diff report sin copiar archivos
- ✅ Indicar qué archivos se copiarían/sobrescribirían
- ✅ No modificar ningún archivo

**Files**:
- `installer/smart_update.py`

**Dependencies**: QUANT-008-007

**Test**:
```bash
python sia/installer/smart_update.py --dry-run
# Expected output:
# [DRY RUN] Would copy: .sia/prompts/new.prompt.md
# [DRY RUN] Would backup: .sia/prompts/activate.prompt.md
# [DRY RUN] Conflict detected: .sia/skills/audit_ddd.py
```

---

### QUANT-008-009: Auto-Discovery Integration
**Estimate**: 2h  
**Phase**: 3 - Auto-Detection  
**Priority**: Medium

**Specification**:
Extender `auto_discovery.py` para detectar updates disponibles.

**Acceptance Criteria**:
- ✅ Comparar `sia/VERSION` vs `.sia/VERSION`
- ✅ Agregar campo `update_available: bool` a `.sia.detected.yaml`
- ✅ Agregar campo `update_version: str` (versión disponible)
- ✅ Ejecutar automáticamente en `smart_init.py`

**Files**:
- `installer/auto_discovery.py` (modify)

**Dependencies**: QUANT-008-001

**Test**:
```yaml
# .sia.detected.yaml expected:
update_available: true
update_version: "1.2.0"
current_version: "1.0.0"
```

---

### QUANT-008-010: Copilot Instructions Warning
**Estimate**: 1h  
**Phase**: 3 - Auto-Detection  
**Priority**: Medium

**Specification**:
Actualizar template de Copilot Instructions para mostrar aviso de update.

**Acceptance Criteria**:
- ✅ Si `update_available: true` → Insertar warning banner
- ✅ Banner: "⚠️ SIA framework update available (1.2.0). Run /update"
- ✅ Template placeholder: `{{UPDATE_WARNING}}`
- ✅ Auto-regenerar instructions en `smart_init.py`

**Files**:
- `core/copilot-instructions.template.md` (modify)
- `installer/auto_discovery.py` (modify `assemble_instructions()`)

**Dependencies**: QUANT-008-009

**Test**:
```markdown
# .github/copilot-instructions.md expected:
⚠️ **Framework Update Available**: SIA 1.2.0 is available (current: 1.0.0)
Run `/update` to sync new capabilities.
```

---

### QUANT-008-011: Update Slash Command
**Estimate**: 1h  
**Phase**: 3 - Auto-Detection  
**Priority**: High

**Specification**:
Crear slash command `/update` en prompts.

**Acceptance Criteria**:
- ✅ Archivo: `templates/prompts/update.prompt.md`
- ✅ Comando: `/update [--dry-run]`
- ✅ Ejecuta: `uv run python sia/installer/smart_update.py`
- ✅ Muestra: Diff report + confirmación

**Files**:
- `templates/prompts/update.prompt.md` (create)

**Dependencies**: QUANT-008-008

**Test**:
```
User: /update
Agent: Executes smart_update.py, shows changes, asks confirmation
```

---

### QUANT-008-012: Rollback Implementation
**Estimate**: 2h  
**Phase**: 4 - Rollback & Safety  
**Priority**: Medium

**Specification**:
Implementar comando de rollback usando backups.

**Acceptance Criteria**:
- ✅ CLI flag: `python smart_update.py --rollback`
- ✅ Leer último entry de SYNC_LOG.md
- ✅ Restaurar archivos desde `.sia/.backups/`
- ✅ Revertir `.sia/VERSION` a versión anterior

**Files**:
- `installer/smart_update.py`

**Dependencies**: QUANT-008-006

**Test**:
```bash
python sia/installer/smart_update.py
# Apply changes...
python sia/installer/smart_update.py --rollback
# Expected: Files restored from .backups/, VERSION reverted
```

---

### QUANT-008-013: Interactive Confirmation
**Estimate**: 1h  
**Phase**: 4 - Rollback & Safety  
**Priority**: Low

**Specification**:
Agregar confirmación interactiva antes de cambios destructivos.

**Acceptance Criteria**:
- ✅ Si hay conflictos → Preguntar: "Apply non-conflicting changes? (y/n)"
- ✅ Si hay overwrites → Preguntar: "Overwrite {count} files? (y/n)"
- ✅ Flag `--yes` para skip confirmación (CI/CD)

**Files**:
- `installer/smart_update.py`

**Dependencies**: QUANT-008-007

**Test**:
```bash
python sia/installer/smart_update.py
# Expected: "5 files will be overwritten. Continue? (y/n)"
```

---

### QUANT-008-014: Idempotency Tests
**Estimate**: 2h  
**Phase**: 4 - Rollback & Safety  
**Priority**: High

**Specification**:
Validar que ejecutar update múltiples veces no causa side-effects.

**Acceptance Criteria**:
- ✅ Ejecutar `smart_update.py` 2 veces consecutivas
- ✅ Segunda ejecución: "Already up to date"
- ✅ No duplicar entradas en SYNC_LOG.md
- ✅ No crear backups innecesarios

**Files**:
- `tests/test_smart_update.py` (create)

**Dependencies**: All previous QUANTs

**Test**:
```bash
python sia/installer/smart_update.py
python sia/installer/smart_update.py
# Expected: "✅ Already up to date (version 1.2.0)"
```

---

### QUANT-008-015: Documentation & Integration
**Estimate**: 1h  
**Phase**: 4 - Rollback & Safety  
**Priority**: Medium

**Specification**:
Documentar nuevo sistema en README y CHANGELOG.

**Acceptance Criteria**:
- ✅ Actualizar `docs/QUICKSTART.md` con sección "Updating SIA"
- ✅ Agregar entrada en `docs/CHANGELOG.md` (version 1.2.0)
- ✅ Actualizar `installer/README.md` con smart_update.py
- ✅ Crear `docs/UPDATE_GUIDE.md` con troubleshooting

**Files**:
- `docs/QUICKSTART.md`
- `docs/CHANGELOG.md`
- `installer/README.md`
- `docs/UPDATE_GUIDE.md` (create)

**Dependencies**: QUANT-008-014

**Test**:
Manual review of documentation completeness.

---

## TASK SUMMARY

**Total Tasks**: 15  
**Total Estimate**: 24 hours  
**Phases**: 4

### By Phase:
- **Phase 1** (Core Logic): 6h - 4 tasks
- **Phase 2** (Merge): 7h - 4 tasks
- **Phase 3** (Auto-Detection): 4h - 3 tasks
- **Phase 4** (Safety): 6h - 4 tasks

### By Priority:
- **High**: 9 tasks (16h)
- **Medium**: 5 tasks (7h)
- **Low**: 1 task (1h)

---

## DEPENDENCY GRAPH

```
QUANT-008-001 (Version Detection)
    ↓
QUANT-008-002 (Diff Detection) ← QUANT-008-005 (Hash Detection)
    ↓                                    ↓
QUANT-008-003 (Simple Copy)      QUANT-008-006 (Backup)
    ↓                                    ↓
QUANT-008-004 (Sync Log) ← QUANT-008-007 (Conflict Detection)
                                         ↓
                               QUANT-008-008 (Dry-Run)
                                         ↓
QUANT-008-009 (Auto-Discovery) → QUANT-008-010 (Copilot Warning)
         ↓
QUANT-008-011 (Slash Command)

QUANT-008-012 (Rollback) ← QUANT-008-006
         ↓
QUANT-008-013 (Confirmation) ← QUANT-008-007
         ↓
QUANT-008-014 (Idempotency Tests)
         ↓
QUANT-008-015 (Documentation)
```

---

## EXECUTION ORDER (Recommended)

**Sprint 1** (8h):
1. QUANT-008-001 (2h)
2. QUANT-008-002 (2h)
3. QUANT-008-003 (1h)
4. QUANT-008-004 (1h)
5. QUANT-008-005 (2h)

**Sprint 2** (8h):
6. QUANT-008-006 (2h)
7. QUANT-008-007 (2h)
8. QUANT-008-008 (1h)
9. QUANT-008-009 (2h)
10. QUANT-008-010 (1h)

**Sprint 3** (8h):
11. QUANT-008-011 (1h)
12. QUANT-008-012 (2h)
13. QUANT-008-013 (1h)
14. QUANT-008-014 (2h)
15. QUANT-008-015 (1h)
16. Buffer/Refinement (1h)

---

**Status**: Ready for implementation  
**Next Action**: Start QUANT-008-001
