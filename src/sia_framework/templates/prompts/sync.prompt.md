---
name: sync
description: Sincronizar .sia/ con actualizaciones del submódulo SIA (tool-based execution)
---

🔄 **FRAMEWORK SYNC PROTOCOL**

Super Agent ejecuta sincronización usando **SOLO tools nativas** (list_dir, read_file, create_file, replace_string_in_file).

---

## FASE 1: DETECCIÓN DE CONTEXTO

**1.1 Verificar Estructura del Submódulo**
```
Tool: list_dir("sia/templates/prompts/")
Expected: *.prompt.md files
```

**1.2 Detectar Versiones**
```
Tool: read_file("sia/VERSION", 1, 1)
Store: framework_version

Tool: read_file(".sia/metadata/sia_version.txt", 1, 1) 
Store: local_version (si existe, sino → primera sync)
```

**1.3 Decisión de Sync**
```
If local_version NOT exists:
  → Primera sincronización (modo bootstrap)
  → Copiar todo sin preguntar

If local_version < framework_version:
  → Actualización disponible
  → Proceder con sync inteligente

If local_version > framework_version:
  → ⚠️ DOWNGRADE detectado
  → Preguntar: "Submódulo más antiguo. ¿Continuar? (y/n)"
  → Si no → ABORT

If local_version == framework_version:
  → Verificar archivos nuevos/modificados de todas formas
```

---

## FASE 2: INVENTARIO DE ARCHIVOS

**2.1 Listar Prompts del Framework**
```
Tool: list_dir("sia/templates/prompts/")
Filter: *.prompt.md only
Store: framework_prompts[] 

Example output:
  activate.prompt.md
  boost.prompt.md
  continue.prompt.md
  debug.prompt.md
  (... etc)
```

**2.2 Listar Prompts Locales**
```
Tool: list_dir(".sia/prompts/")
Filter: *.prompt.md only
Store: local_prompts[]
```

**2.3 Calcular Diferencias**
```
new_prompts = framework_prompts - local_prompts
existing_prompts = framework_prompts ∩ local_prompts
```

---

## FASE 3: SINCRONIZACIÓN INTELIGENTE

### **3.1 Nuevos Prompts (NO existen localmente)**

```
For each file in new_prompts:
  
  Step 1: Copiar archivo directamente (optimización de tokens)
  Tool: run_in_terminal(
    command: f"cp sia/templates/prompts/{filename} .sia/prompts/{filename}",
    explanation: f"Copiar {filename} a prompts locales"
  )
  
  Step 2: Calcular hash para tracking
  Tool: run_in_terminal(
    command: f"shasum -a 256 .sia/prompts/{filename} | awk '{{print $1}}'",
    explanation: "Calcular hash del prompt nuevo"
  )
  Store: file_hash
  
  Step 3: Log
  Report: "✅ NEW: {filename}"
```

### **3.2 Prompts Existentes (Ya están localmente)**

```
For each file in existing_prompts:
  
  Step 1: Leer ambas versiones
  Tool: read_file(f"sia/templates/prompts/{filename}", 1, -1)
  Store: source_content
  
  Tool: read_file(f".sia/prompts/{filename}", 1, -1)
  Store: target_content
  
  Step 2: Comparar contenido
  If source_content == target_content:
    Report: "✅ SYNC: {filename} (sin cambios)"
    CONTINUE to next file
  
  Step 3: Detectar personalización
  Tool: read_file(".sia/metadata/original_hashes.json", 1, -1)
  Parse JSON → original_hashes{}
  
  Tool: run_in_terminal(
    command: f"shasum -a 256 .sia/prompts/{filename} | awk '{{print $1}}'",
    explanation: "Hash actual del archivo local"
  )
  Store: current_hash
  
  original_hash = original_hashes.get(filename, null)
  
  Step 4: Decisión de merge
  
  Case A: current_hash == original_hash (NO personalizado)
    → El archivo local es idéntico a la versión original instalada
    → SEGURO sobrescribir con nueva versión
    
    Tool: replace_string_in_file(
      filePath: f".sia/prompts/{filename}",
      oldString: target_content,
      newString: source_content
    )
    Report: "🔄 UPDATED: {filename}"
  
  Case B: current_hash != original_hash (PERSONALIZADO)
    → Usuario modificó el archivo localmente
    → PREGUNTAR antes de sobrescribir
    
    User prompt: "⚠️ {filename} personalizado. Detectados cambios locales.
                  Opciones:
                  1. Mantener versión local (recomendado)
                  2. Sobrescribir con versión del framework
                  3. Ver diff y decidir
                  
                  ¿Qué hacer? (1/2/3)"
    
    If choice == 1:
      Report: "🔒 PROTECTED: {filename} (personalización preservada)"
      
    If choice == 2:
      Sub-step 1: Crear backup
      Tool: create_file(
        f".sia/backup/{timestamp}/{filename}",
        target_content
      )
      
      Sub-step 2: Sobrescribir
      Tool: replace_string_in_file(
        filePath: f".sia/prompts/{filename}",
        oldString: target_content,
        newString: source_content
      )
      Report: "🔄 OVERWRITTEN: {filename} (backup creado)"
    
    If choice == 3:
      Tool: run_in_terminal(
        command: f"diff -u .sia/prompts/{filename} sia/templates/prompts/{filename}",
        explanation: "Mostrar diferencias"
      )
      → Repeat prompt with options 1/2
  
  Case C: original_hash NOT exists (primera sync o metadata perdida)
    → Asumir potencial personalización (conservador)
    → Preguntar al usuario (mismo flujo que Case B)
```

---

## FASE 4: SINCRONIZAR OTROS COMPONENTES

### **4.1 Skills (`sia/skills/` → `.sia/skills/`)**

**4.1.1 File Readers Module (REQ-011)**
```
Tool: list_dir("sia/templates/skills/file_readers/")
Store: file_reader_modules[]

If file_reader_modules:
  Report: "📚 Detectados file readers en framework"
  
  # Sync file_readers/ module
  For each module_file in file_reader_modules:
    source = f"sia/templates/skills/file_readers/{module_file}"
    target = f".sia/skills/file_readers/{module_file}"
    
    Tool: read_file(source, 1, -1)
    Store: source_content
    
    If NOT exists(target):
      Tool: create_file(target, source_content)
      Report: "✅ NEW MODULE: file_readers/{module_file}"
    Else:
      Tool: read_file(target, 1, -1)
      Store: target_content
      
      If source_content != target_content:
        Tool: replace_string_in_file(target, target_content, source_content)
        Report: "🔄 UPDATED: file_readers/{module_file}"
      Else:
        Report: "✅ SYNC: file_readers/{module_file}"
  
  # Sync CLI facades (read_*.py)
  Tool: list_dir("sia/templates/skills/")
  Filter: read_*.py
  Store: reader_facades[]
  
  For each facade in reader_facades:
    source = f"sia/templates/skills/{facade}"
    target = f".sia/skills/{facade}"
    
    Tool: read_file(source, 1, -1)
    Store: source_content
    
    If NOT exists(target):
      Tool: create_file(target, source_content)
      Tool: run_in_terminal(
        command: f"chmod +x .sia/skills/{facade}",
        explanation: "Hacer ejecutable el reader facade"
      )
      Report: "✅ NEW READER: {facade}"
    Else:
      Tool: read_file(target, 1, -1)
      Store: target_content
      
      If source_content != target_content:
        Tool: replace_string_in_file(target, target_content, source_content)
        Report: "🔄 UPDATED: {facade}"
      Else:
        Report: "✅ SYNC: {facade}"
Else:
  Report: "⚠️  File readers no disponibles en framework (versión <1.2.0)"
```

**4.1.2 Other Skills (Custom)**
```
Tool: list_dir("sia/skills/")
Filter: *.sh, *.py, *.md (excluding README.md, read_*.py)
Store: framework_skills[]

For each skill in framework_skills:
  target_path = f".sia/skills/{skill}"
  
  If NOT exists(target_path):
    Tool: read_file(f"sia/skills/{skill}", 1, -1)
    Tool: create_file(target_path, content)
    Report: "✅ NEW SKILL: {skill}"
  
  Else:
    Report: "🔒 EXISTING: {skill} (no sobrescribir, puede estar personalizado)"
    # Skills existentes NO se actualizan automáticamente (riesgo de personalización)
```

### **4.2 Framework Agents (`sia/agents/` → `.sia/agents/`)**

```
framework_agents = [
  "repository_guardian.md",
  "research_specialist.md",
  "compliance_officer.md",
  "sia.md"
]

For each agent in framework_agents:
  source = f"sia/agents/{agent}"
  target = f".sia/agents/{agent}"
  
  Tool: read_file(source, 1, -1)
  Store: source_content
  
  If NOT exists(target):
    Tool: create_file(target, source_content)
    Report: "✅ NEW AGENT: {agent}"
  
  Else:
    Tool: read_file(target, 1, -1)
    Store: target_content
    
    If source_content != target_content:
      Tool: replace_string_in_file(
        filePath: target,
        oldString: target_content,
        newString: source_content
      )
      Report: "🔄 UPDATED AGENT: {agent}"
    Else:
      Report: "✅ SYNC: {agent}"

# CRÍTICO: NUNCA tocar .sia/agents/{project_name}.md (SPR del proyecto)
```

### **4.3 Templates de Referencia (`sia/templates/` → `.sia/knowledge/`)**

```
reference_templates = [
  "PROJECT_SPR.template.md",
  "DEFAULT_STACK.md"
]

For each template in reference_templates:
  source = f"sia/templates/{template}"
  target = f".sia/knowledge/{template}"
  
  Tool: read_file(source, 1, -1)
  
  If NOT exists(target):
    Tool: create_file(target, content)
    Report: "✅ REFERENCE: {template}"
  # NO sobrescribir si existe (puede tener anotaciones del proyecto)
```

---

## FASE 5: ACTUALIZAR METADATA

### **5.1 Versión Sincronizada**
```
Tool: create_file(".sia/metadata/sia_version.txt", framework_version)
```

### **5.2 Timestamp de Sync**
```
Tool: run_in_terminal(
  command: "date -u +%Y-%m-%dT%H:%M:%SZ",
  explanation: "Obtener timestamp ISO 8601"
)
Store: current_timestamp

Tool: create_file(".sia/metadata/last_sync.txt", current_timestamp)
```

### **5.3 Actualizar Hashes Originales**
```
# Construir JSON con hashes de TODOS los prompts sincronizados
hashes_json = {}

For each prompt in (.sia/prompts/*.prompt.md):
  Tool: run_in_terminal(
    command: f"shasum -a 256 .sia/prompts/{prompt} | awk '{{print $1}}'",
    explanation: f"Hash de {prompt}"
  )
  hashes_json[f"prompts/{prompt}"] = hash_output

# Serializar a JSON
json_content = JSON.stringify(hashes_json, indent=2)

# Guardar
Tool: create_file(".sia/metadata/original_hashes.json", json_content)
```

### **5.4 Log de Sincronización**
```
log_entry = f"""
[{current_timestamp}] SYNC COMPLETED
Framework: {local_version} → {framework_version}
New prompts: {len(new_prompts)}
Updated prompts: {count_updated}
Protected prompts: {count_protected}
New skills: {count_new_skills}
Updated agents: {count_updated_agents}
---
"""

Tool: read_file(".sia/metadata/sync.log", 1, -1) if exists
Append log_entry to content
Tool: create_file(".sia/metadata/sync.log", updated_content)
```

---

## FASE 6: REPORTE FINAL

```
Output to user:

🔄 **SINCRONIZACIÓN COMPLETADA**

**Prompts:**
  ✅ NEW: boost.prompt.md
  ✅ NEW: handoff.prompt.md
  🔄 UPDATED: debug.prompt.md (hash mismatch → actualizado)
  🔒 PROTECTED: quant.prompt.md (personalización detectada)
  ✅ SYNC: 8 archivos sin cambios

**Skills:**
  ✅ NEW: audit_dependencies.sh
  🔒 EXISTING: 12 skills preservados

**Agents:**
  🔄 UPDATED: repository_guardian.md
  🔄 UPDATED: research_specialist.md
  🔒 PROTECTED: myproject.md (SPR del proyecto)

**Framework Version:** {local_version} → {framework_version}
**Last Sync:** {current_timestamp}

---

💡 **Archivos Protegidos:** Los prompts personalizados se preservaron automáticamente.
   Para forzar actualización: Eliminar archivo y ejecutar /sync nuevamente.

📦 **Backup:** Archivos sobrescritos → `.sia/backup/{timestamp}/`
```

---

## VARIANTES DEL COMANDO

### **`/sync --dry-run`** (Simulación)
```
Execute FASE 1-3 pero:
- NO crear archivos (skip create_file)
- NO sobrescribir (skip replace_string_in_file)
- SOLO reportar qué haría

Output: Lista de cambios pendientes sin aplicar
```

### **`/sync --force`** (Sobrescribir TODO)
```
Step 1: Confirmar con usuario
"⚠️ FORCE MODE sobrescribirá TODAS las personalizaciones.
 ¿Estás seguro? (escribe 'CONFIRMAR' para continuar)"

If confirmed:
  - Ignorar detección de personalización
  - Sobrescribir todos los archivos existentes
  - Crear backups en .sia/backup/{timestamp}/
  
Else:
  ABORT
```

### **`/sync rollback`** (Restaurar Backup)
```
Step 1: Listar backups disponibles
Tool: list_dir(".sia/backup/")
Store: backup_dirs[] (sorted by timestamp descending)

Step 2: Mostrar al usuario
"Backups disponibles:
 1. 2025-11-29T14-30-00 (hace 2 horas)
 2. 2025-11-28T10-15-00 (hace 1 día)
 
 ¿Cuál restaurar? (1/2)"

Step 3: Restaurar
For each file in selected_backup:
  Tool: read_file(f".sia/backup/{timestamp}/{file}", 1, -1)
  Tool: replace_string_in_file or create_file → Restore to .sia/

Step 4: Actualizar metadata
Tool: create_file(".sia/metadata/sia_version.txt", backup_version)

Report: "✅ Restaurado a estado del {timestamp}"
```

---

## EDGE CASES CRÍTICOS

### **EC-1: Primera Sincronización**
```
If NOT exists(".sia/metadata/sia_version.txt"):
  → Bootstrap mode
  → Copiar TODO sin preguntar
  → Crear metadata inicial con hashes de todos los archivos
  → Report: "📦 Primera sincronización completada"
```

### **EC-2: Metadata Corrupta/Perdida**
```
If exists(".sia/metadata/original_hashes.json"):
  Try parse JSON
  If parse error:
    → Regenerar metadata
    → Asumir todos los archivos como potencialmente personalizados
    → Preguntar para cada archivo existente
```

### **EC-3: Submódulo Sin Actualizar**
```
Before FASE 1:
Tool: run_in_terminal(
  command: "git -C sia rev-parse HEAD",
  explanation: "Verificar commit del submódulo"
)
Store: current_commit

Tool: run_in_terminal(
  command: "git -C sia rev-parse @{u}",
  explanation: "Commit remoto del submódulo"
)
Store: remote_commit

If current_commit != remote_commit:
  Report: "⚠️ Submódulo sia/ desactualizado.
          Ejecuta primero: git submodule update --remote sia
          
          ¿Continuar de todas formas? (y/n)"
  
  If no → ABORT
```

### **EC-4: Archivos Huérfanos (locales pero no en framework)**
```
orphan_prompts = local_prompts - framework_prompts

If orphan_prompts NOT empty:
  Report: "⚠️ Prompts locales sin equivalente en framework:
          {list(orphan_prompts)}
          
          Estos son prompts creados localmente o eliminados del framework.
          ¿Qué hacer?
          1. Mantener (recomendado)
          2. Mover a .sia/prompts/_archive/
          3. Eliminar
          
          Opción: (1/2/3)"
```

---

## ANTI-PATRONES ❌

1. **NO ejecutar scripts Python** → Todo via tools nativas
2. **NO sobrescribir** `.sia/agents/{project}.md` → Es único del proyecto
3. **NO perder backups** → Siempre crear antes de sobrescribir
4. **NO sincronizar** `.sia.detected.yaml` → Específico del proyecto
5. **NO asumir** → Siempre preguntar en conflictos (UX conversacional)

---

## PRINCIPIOS DE DISEÑO ✅

- **DDD**: Bounded context claro (framework sync ≠ project files)
- **SOLID**: Single Responsibility (cada fase hace UNA cosa)
- **KISS**: Lógica simple, sin abstracciones innecesarias
- **CLEAN CODE**: Instrucciones legibles, pasos explícitos
- **Δ(Framework) ⇒ Δ(.sia/)**: Sincronización atómica y trazable

---

## VALIDACIÓN POST-SYNC

```
Super Agent verifica:

1. Metadata actualizada
   Tool: read_file(".sia/metadata/sia_version.txt", 1, 1)
   Assert: == framework_version

2. Hashes guardados
   Tool: read_file(".sia/metadata/original_hashes.json", 1, -1)
   Assert: Valid JSON, contiene >= len(synced_prompts) entries

3. Backup creado (si hubo sobrescrituras)
   Tool: list_dir(f".sia/backup/{timestamp}/")
   Assert: Contains overwritten files

4. Log actualizado
   Tool: read_file(".sia/metadata/sync.log", -5, -1)
   Assert: Last entry timestamp == current_timestamp
```

---

**STATUS**: Ready for Super Agent execution
**DEPENDENCIES**: None (pure tool-based)
**EXECUTION TIME**: ~2-5 min (interactive, depends on conflicts)
