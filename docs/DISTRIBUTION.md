# SIA Framework - Guía de Distribución

**Para Colegas y Nuevos Usuarios**

## ¿Qué es SIA?

**SIA (Super Intelligence Agency)** es un framework meta-cognitivo que convierte GitHub Copilot en un "Super Agente" capaz de:

✅ **Auto-descubrir** la arquitectura de cualquier proyecto  
✅ **Enforcar DDD/SOLID** con guardianes automáticos  
✅ **Gestionar requerimientos** con ciclo QUANT de 7 fases  
✅ **Analizar código** (complejidad, cobertura, dependencias)  
✅ **Razonar sobre arquitectura** antes de implementar  

## Instalación Rápida (2 minutos)

### Paso 1: Requisitos Previos

- Python 3.10+ con `uv` o `uvx`
- GitHub Copilot (suscripción requerida)

**Instalar uv (si no lo tienes):**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

### Paso 2: Instalar SIA

```bash
# En la raíz de tu proyecto
uvx --from git+https://github.com/gpilleux/sia.git sia-framework init
```

¡Eso es todo! ✅

### Paso 3: Verificar Instalación

```bash
# Verificar archivos generados
ls -la .sia.detected.yaml
ls -la .github/copilot-instructions.md
ls -la .sia/

# Revisar configuración detectada
cat .sia.detected.yaml
```

### Otros Comandos

```bash
# Actualizar copilot-instructions.md
uvx --from git+https://github.com/gpilleux/sia.git sia-framework update

# Verificar salud de la instalación
uvx --from git+https://github.com/gpilleux/sia.git sia-framework doctor
```

## ¿Qué Hace el Instalador?

El instalador ejecuta **auto-discovery** en tu proyecto:

1. **Detecta identidad Git:**
   - Nombre del proyecto
   - Owner/Organization
   - Repository URL

2. **Identifica tech stack:**
   - Python, Node, FastAPI, Next.js, etc.
   - DDD, MVC, u otra arquitectura

3. **Extrae bounded contexts:**
   - Escanea `domain/` para encontrar contextos
   - Analiza `api/` routers como fallback

4. **Genera configuración:**
   - Crea `.sia.detected.yaml` con toda la metadata
   - Actualiza `.github/copilot-instructions.md` con SIA

5. **Instala herramientas:**
   - Slash commands en `.sia/prompts/`
   - File readers (DOCX, XLSX, PDF) en `.sia/skills/`

## Estructura del Proyecto Post-Instalación

```
tu-proyecto/
├── .sia/                       # ✅ Directorio SIA del proyecto
│   ├── agents/                 # Agentes específicos del proyecto
│   ├── knowledge/              # Base de conocimiento
│   ├── requirements/           # Gestión de requerimientos
│   ├── skills/                 # Scripts y herramientas
│   └── prompts/                # Slash commands
├── .sia.detected.yaml          # ✅ Config auto-generada
├── .github/
│   └── copilot-instructions.md # ✅ Instrucciones mejoradas con SIA
├── .vscode/
│   └── settings.json           # ✅ Configuración VS Code
└── ... (tu código existente)
```

## Casos de Uso

### 1. Nuevo Requerimiento

**Antes (sin SIA):**
```
Tú: "Necesito agregar autenticación JWT"
Copilot: [genera código directo sin análisis]
```

**Después (con SIA):**
```
Tú: "Necesito agregar autenticación JWT"
SIA: 
  1. Traduce a REQ-XXX formal
  2. Analiza bounded contexts impactados
  3. Descompone en tareas QUANT
  4. Guía implementación DDD
  5. Valida arquitectura post-cambio
```

### 2. Gestión de Requerimientos

SIA implementa ciclo QUANT de 7 fases:

```
requirements/
├── REQ-001/
│   ├── REQ-001.md                  # Requerimiento formal
│   ├── REQ-001_domain_analysis.md  # Análisis de dominio
│   └── REQ-001_quant_breakdown.md  # Desglose de tareas
├── REQ-002/
└── _archive/                       # REQs completados
```

## Configuración Avanzada

### .sia.detected.yaml

Ejemplo de configuración auto-generada:

```yaml
sia_version: 1.0.0

project:
  name: mi-proyecto
  type: python-fastapi-ddd
  owner: mi-empresa
  repo: mi-proyecto
  
domain:
  bounded_contexts:
    - Users
    - Products
    - Orders
    
spr:
  path: .agents/mi-proyecto.md
  
agents:
  active:
    - requirement_translator
    - domain_extractor
    - repository_guardian
```

### Personalización

Puedes editar `.sia.detected.yaml` manualmente para:
- Agregar bounded contexts custom
- Habilitar/deshabilitar agentes específicos
- Configurar parámetros de skills

## Troubleshooting

### Error: "uv: command not found"

**Solución:**
```bash
pip3 install uv
# o
python3 -m pip install uv
```

### Error: "Python not found" (Windows)

**Solución:**
1. Reinstalar Python desde python.org
2. ✅ Marcar "Add Python to PATH"
3. Reiniciar Command Prompt

### Error: "Permission denied" (macOS/Linux)

**Solución:**
```bash
python3 sia/installer/install.py
```

### Auto-discovery falla

**Configuración manual:**
```bash
# Copiar template
cp sia/core/sia.detected.template.yaml .sia.detected.yaml

# Editar con tus detalles
nano .sia.detected.yaml
```

## Actualización del Framework

```bash
cd sia
git pull origin main
cd ..
git add sia
git commit -m "chore: Update SIA framework to latest version"
git push
```

## Ejemplos de Proyectos Usando SIA

### Argus (AI Document Intelligence)
- **Repo**: https://github.com/gpilleux/argus
- **Stack**: Python + FastAPI + PostgreSQL + pgvector + Google ADK
- **Bounded Contexts**: Documents, Chat, Visualization
- **Learnings**: Ver `.sia/agents/argus.md` → "PROJECT LEARNINGS"

### [Tu Proyecto Aquí]
- **Repo**: TBD
- **Stack**: TBD
- **Bounded Contexts**: TBD

## Recursos

- **Documentación completa**: [sia/QUICKSTART.md](./sia/QUICKSTART.md)
- **Repositorio SIA**: https://github.com/gpilleux/sia
- **Issues**: https://github.com/gpilleux/sia/issues
- **Ejemplos**: `sia/examples/` (TBD)

## Contribuir al Framework

Si descubres mejoras aplicables a TODOS los proyectos:

1. **Framework Learning**: Dile a Copilot "Aprende esto como framework..."
2. SIA pedirá confirmación antes de commit a `sia/` submodule
3. Push al repositorio central: https://github.com/gpilleux/sia

**Tipos de contribuciones:**
- ✅ Nuevas skills genéricas (`sia/skills/`)
- ✅ Templates de agentes mejorados (`sia/agents/`)
- ✅ Estándares de arquitectura (`sia/core/`)
- ❌ NO: Código específico de producto

## Soporte

**Preguntas frecuentes**: Ver `sia/QUICKSTART.md`  
**Bugs**: https://github.com/gpilleux/sia/issues  
**Contacto**: [tu-email@empresa.com]

---

## Checklist de Onboarding

- [ ] Requisitos instalados (Python 3.10+, Git, uv)
- [ ] Submodule agregado (`git submodule add ...`)
- [ ] Instalador ejecutado (`python3 sia/installer/install.py`)
- [ ] Verificar `.sia.detected.yaml` generado
- [ ] Revisar `.github/copilot-instructions.md`
- [ ] Probar skill: `sh sia/skills/check_complexity.sh`
- [ ] Crear primer requerimiento con Copilot
- [ ] Leer documentación completa (`sia/QUICKSTART.md`)

---

**¡Bienvenido a SIA!** 🚀

Empieza diciendo a GitHub Copilot: *"Muéstrame qué detectó SIA sobre mi proyecto"*
