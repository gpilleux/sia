---
name: sync-instructions
description: Actualizar .github/copilot-instructions.md con secciones core de SIA framework
---

🔄 **COPILOT INSTRUCTIONS SYNC PROTOCOL**

Actualiza `.github/copilot-instructions.md` con secciones core del framework SIA, preservando contenido específico del proyecto.

---

## OBJETIVO

Sincronizar únicamente las **secciones core** de SIA framework en `copilot-instructions.md`:
- **EXECUTION ENVIRONMENT** - Autoconciencia del ambiente VS Code
- Otros meta-patterns del framework (futuro)

**NO tocar**:
- Contenido específico del proyecto
- Configuraciones personalizadas
- Secciones fuera del scope core

---

## FASE 1: VERIFICACIÓN

**1.1 Verificar Existencia de Archivos**
```
Tool: read_file(".github/copilot-instructions.md", 1, 30)
Store: current_instructions_header

Tool: read_file("sia/core/copilot-instructions.template.md", 1, 50)
Store: template_environment_section
```

**1.2 Detectar Versión del Framework**
```
Tool: read_file("sia/VERSION", 1, 1)
Store: framework_version
```

**1.3 Verificar si Necesita Sync**
```
Search in current_instructions_header for "## EXECUTION ENVIRONMENT"

If NOT found:
  → Primera vez, insertar sección completa
  
If found:
  → Verificar si contenido coincide con template
  → Si difiere → Actualizar
  → Si igual → Skip (ya sincronizado)
```

---

## FASE 2: EXTRACCIÓN DE SECCIÓN CORE

**2.1 Extraer Sección EXECUTION ENVIRONMENT del Template**
```
Tool: read_file("sia/core/copilot-instructions.template.md", 1, 50)
Expected content:
  ## EXECUTION ENVIRONMENT
  **Runtime**: Visual Studio Code + GitHub Copilot Chat
  **Agent**: Claude Sonnet 4.5 (via GitHub Copilot)
  ... (resto de la sección)
  ---

Store: environment_section (desde "## EXECUTION ENVIRONMENT" hasta el "---" siguiente)
```

---

## FASE 3: SINCRONIZACIÓN INTELIGENTE

### **3.1 Caso: Sección NO existe (Primera Inserción)**

```
Step 1: Leer encabezado del archivo actual
Tool: read_file(".github/copilot-instructions.md", 1, 5)
Expected: 
  # PROJECT_NAME - ...
  # GitHub Copilot Instructions

Step 2: Insertar sección EXECUTION ENVIRONMENT después del header
Tool: replace_string_in_file(
  filePath: ".github/copilot-instructions.md",
  oldString: "# PROJECT_NAME - ...\n# GitHub Copilot Instructions\n\n## META-SYSTEM",
  newString: "# PROJECT_NAME - ...\n# GitHub Copilot Instructions\n\n## EXECUTION ENVIRONMENT\n[contenido extraído del template]\n---\n\n## META-SYSTEM"
)

Output: ✅ Sección EXECUTION ENVIRONMENT insertada
```

### **3.2 Caso: Sección existe (Actualización)**

```
Step 1: Leer sección actual completa
Tool: grep_search(
  query: "## EXECUTION ENVIRONMENT",
  includePattern: ".github/copilot-instructions.md"
)
Store: current_line_number

Tool: read_file(".github/copilot-instructions.md", current_line_number, current_line_number + 30)
Store: current_environment_section (hasta el siguiente "---")

Step 2: Comparar con template
If current_environment_section == template_environment_section:
  → Output: ℹ️ Sección ya está sincronizada (version {framework_version})
  → SKIP sync
  
If different:
  → Proceder con reemplazo
  
Step 3: Reemplazar sección completa
Tool: replace_string_in_file(
  filePath: ".github/copilot-instructions.md",
  oldString: current_environment_section,
  newString: template_environment_section
)

Output: ✅ Sección EXECUTION ENVIRONMENT actualizada a framework v{framework_version}
```

---

## FASE 4: VERIFICACIÓN POST-SYNC

**4.1 Verificar Integridad del Archivo**
```
Tool: read_file(".github/copilot-instructions.md", 1, 50)
Verify:
  ✅ Header intacto
  ✅ Sección EXECUTION ENVIRONMENT presente
  ✅ Formato correcto (Markdown válido)
  ✅ Sección siguiente intacta (META-SYSTEM o equivalente)
```

**4.2 Calcular Hash de la Sección Sincronizada**
```
Tool: run_in_terminal(
  command: "sed -n '/## EXECUTION ENVIRONMENT/,/^---$/p' .github/copilot-instructions.md | shasum -a 256",
  explanation: "Calcular hash de sección sincronizada"
)
Store: section_hash
```

**4.3 Registrar Sync en Metadata**
```
Tool: create_file(".sia/metadata/instructions_sync.log", 
  content: f"Framework Version: {framework_version}\n
            Sync Date: {current_datetime}\n
            Section Hash: {section_hash}\n
            Status: ✅ Sincronizado"
)
```

---

## OUTPUT ESPERADO

### **Sync Exitoso (Primera Vez)**
```
🔄 Sincronizando copilot-instructions.md con SIA framework v1.1.0...

✅ Sección EXECUTION ENVIRONMENT insertada
   - Runtime awareness añadido
   - MCP server integration documentado
   - VS Code capabilities especificadas

📝 Metadata actualizada: .sia/metadata/instructions_sync.log
```

### **Sync Exitoso (Actualización)**
```
🔄 Sincronizando copilot-instructions.md con SIA framework v1.1.0...

✅ Sección EXECUTION ENVIRONMENT actualizada
   - Cambios detectados desde última sync
   - Framework capabilities actualizadas

📝 Metadata actualizada: .sia/metadata/instructions_sync.log
```

### **Ya Sincronizado**
```
🔄 Verificando copilot-instructions.md...

ℹ️ Sección EXECUTION ENVIRONMENT ya sincronizada (v1.1.0)
   Hash: a3f2c8d9... (sin cambios)
   
✨ No se requiere actualización
```

---

## ANTI-PATTERNS

- ❌ **Sobrescribir contenido del proyecto**: Solo actualizar secciones core de SIA
- ❌ **Sync sin verificación**: Siempre comparar antes de reemplazar
- ❌ **Perder formato**: Mantener estructura Markdown correcta
- ❌ **No verificar integridad**: Confirmar que archivo queda válido post-sync
- ❌ **Sync sin metadata**: Registrar cada sincronización en log

---

## VARIABLES REQUERIDAS

| Variable | Source | Example |
|----------|--------|---------|
| `framework_version` | `sia/VERSION` | `1.1.0` |
| `template_environment_section` | `sia/core/copilot-instructions.template.md` | Sección completa |
| `current_environment_section` | `.github/copilot-instructions.md` | Sección actual (si existe) |
| `section_hash` | Hash SHA256 de sección | `a3f2c8d9...` |

---

## MODO DRY-RUN (Opcional)

```
User: /sync instructions --dry-run

Output:
🔍 DRY-RUN: Verificando cambios sin aplicar...

📋 Cambios detectados:
   - Sección EXECUTION ENVIRONMENT desactualizada
   - Diff: +5 líneas (nuevas capabilities)
   
✨ Ejecutar /sync instructions para aplicar cambios
```

---

## TROUBLESHOOTING

**Problema**: Sección no encontrada en template
**Solución**: Verificar que `sia/core/copilot-instructions.template.md` existe y contiene sección EXECUTION ENVIRONMENT

**Problema**: Archivo copilot-instructions.md no existe
**Solución**: Primero ejecutar instalación de SIA o crear archivo base

**Problema**: Sync rompe formato Markdown
**Solución**: Verificar que sección del template tiene `---` al final para separación correcta

---

**Status**: ✅ Ready  
**Scope**: Solo secciones core de SIA (actualmente EXECUTION ENVIRONMENT)  
**Safety**: Preserva contenido específico del proyecto  
**Idempotente**: Ejecutable múltiples veces sin efectos adversos
