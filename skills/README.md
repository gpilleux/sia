# SIA Skills - Task Performance Tracking

---

## ACTIVE SKILL

**`task_timer.py`** - QUANT task chronometer with AI vs Human comparison

**Purpose**: Track actual execution time vs AI estimates, measure Super Agent performance

**Usage**:
```bash
# Start timer (AI estimates 3h for task)
uv run skills/task_timer.py start QUANT-040 3 "Implement chat UI"

# Check progress
uv run skills/task_timer.py status

# Stop timer (Human team would need 12h)
uv run skills/task_timer.py stop --human-hours 12

# View performance report
uv run skills/task_timer.py metrics
```

**Metrics Tracked**:
- AI Estimated vs Actual (variance %)
- Human Team Estimated vs AI Actual (speedup factor)
- Historical correction factor for future predictions
- Task completion rate

**Integration**: QUANT workflow FASE 5 (execution tracking)

**Docs**: [task_timer.md](task_timer.md)

---

## EXPERT AGENT CREATION

**Tools for generating domain-specific agents**:

- `create_expert_agent.md` - Template and guidelines
- `create_agent_cli.py` - CLI scaffolding generator
- `EXPERT_AGENT_CREATION_QUICKSTART.md` - 5-min guide
- `EXPERT_AGENT_CREATION_SUMMARY.md` - Pattern reference

**Status**: Active (framework meta-tooling)

---

## FILE READERS

**Extract text from documents without manual dependency installation**

File Readers system (REQ-011) provides zero-setup text extraction from DOCX, XLSX, and PDF files using ephemeral dependencies via `uv`.

### Quick Start (No Technical Knowledge Required)

**Read Word documents**:
```bash
uv run skills/read_docx.py report.docx > report_text.txt
```

**Read Excel spreadsheets**:
```bash
uv run skills/read_xlsx.py data.xlsx > data_text.txt
```

**Read PDF files**:
```bash
uv run skills/read_pdf.py invoice.pdf > invoice_text.txt
```

### Advanced Usage (Auto-detect format)

```bash
# Universal reader (detects format automatically)
uv run skills/read_file.py document.docx
uv run skills/read_file.py spreadsheet.xlsx
uv run skills/read_file.py report.pdf

# List supported formats
uv run skills/read_file.py --list-formats
```

### Supported Formats

- **DOCX**: Microsoft Word (text, tables, headers, footers)
- **XLSX**: Microsoft Excel (all sheets, merged cells)
- **PDF**: Adobe PDF (text extraction, natural reading order)

### Error Handling

**File not found**:
```bash
$ uv run skills/read_docx.py noexiste.docx
Error: File not found: noexiste.docx
```

**Corrupted file**:
```bash
$ uv run skills/read_xlsx.py corrupted.xlsx
Error: Corrupted XLSX file: Bad ZIP file
```

**Password-protected**:
```bash
$ uv run skills/read_pdf.py encrypted.pdf
Error: Password-protected PDFs require password parameter
```

### Batch Processing

**Process multiple files**:
```bash
for file in documents/*.docx; do
    uv run skills/read_docx.py "$file" > "text/${file%.docx}.txt"
done
```

### Technical Notes

- **Zero setup**: `uv` installs dependencies automatically (python-docx, openpyxl, PyMuPDF)
- **Memory efficient**: Uses streaming for large files
- **Extensible**: Add new formats by creating readers in `file_readers/`
- **Exit codes**: 0=success, 1=file error, 2=unexpected error
- **Output separation**: stdout=text, stderr=errors

**Implementation**: `file_readers/` module + CLI facades (`read_*.py`)

**Documentation**: `.sia/requirements/REQ-011/` (domain analysis, QUANT breakdown)

---

**Philosophy**: Minimal tooling, maximum leverage. Use platform capabilities over custom scripts.
