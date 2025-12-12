# NEXT SESSION: REQ-011 File Reader Skills System - COMPLETADO

**Quick Start**: `/activate` + "Archivar REQ-011 y crear release notes"

---

## ONE-LINER

✅ **REQ-011 COMPLETADO (2025-12-12)** - File Reader Skills System implementado (DOCX/XLSX/PDF), installers sincronizados, documentación publicada. Pendiente: archival + CHANGELOG release.

---

## CONTEXT RECALL

**Requirement**: File Reader Skills System  
**Status**: ✅ REQ-011 COMPLETADO (6/6 QUANTs)  
**Final Phase**: Archive + Release Notes

**Completado en sesiones anteriores**:

### QUANT-011-001 → Research + Prototypes (2025-12-11)
- ✅ MCP Deepwiki research (python-docx, PyMuPDF, cpython)
- ✅ Prototypes validados (3/3 PASS)
- ✅ Architecture design (Strategy + Registry)

### QUANT-011-002 → Core Module + Registry (2025-12-11)
- ✅ `file_readers/base.py` (AbstractFileReader)
- ✅ Auto-discovery registry (__init_subclass__)
- ✅ Error hierarchy (4 custom exceptions)
- ✅ 96% test coverage

### QUANT-011-003 → Concrete Readers (2025-12-11)
- ✅ DocxReader (iter_inner_content)
- ✅ XlsxReader (read_only mode)
- ✅ PdfReader (get_text sort=True)
- ✅ Edge case handling (corrupted, password-protected)

### QUANT-011-004 → CLI Facades (2025-12-11)
- ✅ read_docx.py, read_xlsx.py, read_pdf.py
- ✅ Ephemeral dependencies (uv --with)
- ✅ Exit codes + output separation
- ✅ Executable permissions

### QUANT-011-005 → Universal CLI (2025-12-11)
- ✅ read_file.py (auto-detect format)
- ✅ --list-formats, --format override
- ✅ UnsupportedFormatError handling
- ✅ Combined dependencies shebang

### QUANT-011-006 → Integration + Docs (2025-12-12) ⭐
- ✅ Installers updated (install.sh, install.bat, install.py)
- ✅ /sync prompt extended (FASE 4.1 Skills)
- ✅ skills/README.md (+89 lines, non-technical)
- ✅ CHANGELOG.md entry (REQ-011 complete)
- ✅ Isolated testing (100% success)

**Evidencia Final**:
```bash
.sia/skills/
├── file_readers/
│   ├── __init__.py
│   ├── base.py
│   ├── docx_reader.py
│   ├── pdf_reader.py
│   └── xlsx_reader.py
├── read_docx.py
├── read_file.py
├── read_pdf.py
└── read_xlsx.py

$ uv run skills/read_file.py --list-formats
Supported formats: docx, pdf, xlsx
```

**Completion Reports**: `.sia/requirements/REQ-011/QUANT_011-{001-006}_COMPLETION.md`


---

## QUANT BREAKDOWN

**Total Tasks**: 6  
**Progress**: 100% (6/6 completed) ✅  
**Total Time**: AI 19h / Human 65h (3.4x speedup)

### All Tasks Completed
1. ✅ **QUANT-011-001** (3h) - Research + Prototypes [2025-12-11]
2. ✅ **QUANT-011-002** (4h) - Core Module + Registry [2025-12-11]
3. ✅ **QUANT-011-003** (5h) - Concrete Readers [2025-12-11]
4. ✅ **QUANT-011-004** (2h) - CLI Facades [2025-12-11]
5. ✅ **QUANT-011-005** (3h) - Universal CLI [2025-12-11]
6. ✅ **QUANT-011-006** (2h) - Integration + Docs [2025-12-12]

### REQ-011 CLOSURE PROTOCOL

**Next Steps**:
1. **Archive REQ-011** → Move to `.sia/requirements/_archive/REQ-011/`
2. **Version Bump** → Update `VERSION` file (1.1.0 → 1.2.0)
3. **Release Notes** → Transform CHANGELOG [Unreleased] → [1.2.0]
4. **Commit Strategy** → Atomic commit with REQ-011 tag
5. **Distribution** → Update git submodules in consumer projects

---

## ARCHIVAL CHECKLIST

**Before moving to `_archive/`**:

### Documentation Verification
- [x] All 6 QUANT completion reports exist
- [x] REQ-011_quant_breakdown.md updated (100% progress)
- [x] NEXT_SESSION.md updated (closure protocol)
- [x] CHANGELOG.md entry complete
- [x] skills/README.md user documentation

### Code Quality
- [x] All files created/modified committed
- [x] Syntax validation (bash -n, py_compile)
- [x] Isolated testing (100% success)
- [x] Cross-platform compatibility verified

### Integration
- [x] Installers sync file_readers/
- [x] /sync prompt supports file_readers
- [x] Documentation accessible to non-technical users

### Metrics
- **Files Created**: 10 (6 module + 4 CLI)
- **Files Modified**: 6 (3 installers + sync + README + CHANGELOG)
- **Test Coverage**: 96% (core), 85%+ (readers)
- **Execution Time**: 19h AI (vs 65h Human) = 3.4x speedup
- **Acceptance Criteria**: 100% (30/30 AC across 6 QUANTs)

### Archive Command
```bash
mv .sia/requirements/REQ-011 .sia/requirements/_archive/
echo "REQ-011 archived $(date +%Y-%m-%d)" >> .sia/requirements/_archive/ARCHIVE_LOG.md
        sys.exit(0)
    
    # Auto-detect or force format
    if args.format:
        reader_class = AbstractFileReader.registry.get(args.format)
    else:
        reader = AbstractFileReader.get_reader(filepath)
```

**Dependency Management**:
- Combine ALL libraries in shebang: `--with python-docx --with openpyxl --with PyMuPDF`
- Registry auto-discovery: `AbstractFileReader.registry` (populated by imports)
- Error handling: UnsupportedFormatError for unknown extensions


---

## INVARIANTS TO VERIFY (QUANT-011-005)

```
read_file.auto_detects(filepath) → Reader | UnsupportedFormatError
∧ read_file.list_formats() → AbstractFileReader.registry.keys()
∧ read_file.dependencies = ⋃ {python-docx, openpyxl, PyMuPDF}
∧ read_file.format_override(--format xlsx, file.xls) → XlsxReader

∀ ext ∈ AbstractFileReader.registry:
  read_file.supports(f"file.{ext}") = TRUE
```

  ∧ facade.executable = TRUE
  ∧ facade.args = {filepath, --help, --version}
  ∧ facade.exit_codes ∈ {0, 1, 2}
  ∧ facade.stdout = extracted_text
  ∧ facade.stderr = error_messages
```

---

## ACCEPTANCE CRITERIA (QUANT-011-004)

- [ ] **AC1**: `uv run skills/read_docx.py file.docx` ejecuta sin instalar globalmente
  - Verification: `which python-docx # No encontrado` + `uv run skills/read_docx.py test.docx # Funciona`
- [ ] **AC2**: Archivos ejecutables con permisos +x
  - Verification: `ls -l skills/read_*.py | grep 'x'`
- [ ] **AC3**: --help muestra usage message claro
  - Verification: `uv run skills/read_docx.py --help` contiene "Extract text from DOCX"
- [ ] **AC4**: Exit codes correctos (0=success, 1=file error, 2=unexpected)
  - Verification: `uv run skills/read_docx.py noexiste.docx; echo $? # 1`
- [ ] **AC5**: stderr para errores, stdout para texto
  - Verification: `uv run skills/read_docx.py corrupted.docx 2>&1 >/dev/null | grep "Error"`

---

## REFERENCES

- **REQ-011**: `.sia/requirements/REQ-011/REQ-011.md`
- **Domain Analysis**: `.sia/requirements/REQ-011/REQ-011_domain_analysis.md`
- **QUANT Breakdown**: `.sia/requirements/REQ-011/REQ-011_quant_breakdown.md`
- **QUANT-001 Completion**: `.sia/requirements/REQ-011/QUANT_011-001_COMPLETION.md`
- **QUANT-002 Completion**: `.sia/requirements/REQ-011/QUANT_011-002_COMPLETION.md`
- **QUANT-003 Completion**: `.sia/requirements/REQ-011/QUANT_011-003_COMPLETION.md`
- **Concrete Readers**: `templates/skills/file_readers/{docx,xlsx,pdf}_reader.py`

- **REQ-011**: `.sia/requirements/REQ-011/REQ-011.md`
- **Domain Analysis**: `.sia/requirements/REQ-011/REQ-011_domain_analysis.md`
- **QUANT Breakdown**: `.sia/requirements/REQ-011/REQ-011_quant_breakdown.md`
- **UV Standard**: `core/UV_STANDARD.md`
- **Skills README**: `skills/README.md`
