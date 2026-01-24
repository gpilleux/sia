---
name: extract
description: Extrae y persiste contenido de DOCX, XLSX, PDF en .sia/docs
argument-hint: "<filepath>"
---

**PROTOCOLO:**
1. Extrae texto usando `.sia/skills/read_file.py`
2. Persiste contenido literal en `.sia/docs/<basename>.txt`
3. Confirma persistencia (sin mostrar contenido)

**EJECUCIÓN:**
```bash
uv run --with python-docx --with openpyxl --with PyMuPDF .sia/skills/read_file.py '<filepath>' > .sia/docs/<basename>.txt 2>&1
```

**OUTPUT:** 
- ✅ Confirmación ruta archivo persistido
- 📊 Estadísticas básicas (bytes, líneas)
- ⚠️ NO mostrar contenido completo

**NOTA:** Para consultar contenido extraído, usar herramientas de lectura estándar sobre archivo persistido.

**GUARDIANES:** DDD | SOLID | Δ(Input) ⇒ Δ(Artifact) | Silence by Default