# SIA Auto-Discovery Protocol
**Bootstrap Sequence for Zero-Configuration Intelligence**

## OVERVIEW
The Auto-Discovery Protocol allows SIA to bootstrap itself within any repository without manual configuration. It scans the environment, detects the project identity, technology stack, and domain structure, and generates a configuration file that adapts the framework to the specific context.

---

## BOOTSTRAP SEQUENCE

### 1. Identity Detection
**Goal**: Determine the project name and origin.
**Mechanism**:
1. Read `.git/config` to find the `remote "origin"` URL.
2. Extract the repository name (e.g., `dipres_analyzer` from `github.com/gpilleux/dipres_analyzer.git`).
3. Fallback: Use the root directory name.

### 2. Technology Stack Detection
**Goal**: Identify the programming language, framework, and architectural pattern.
**Mechanism**:
- Scan for key files:
    - `pyproject.toml` + `fastapi` dependency → `python-fastapi`
    - `package.json` + `react` dependency → `node-react`
    - `go.mod` → `go`
- Scan for directory patterns:
    - `domain/` + `infrastructure/` → `ddd`
    - `app/` + `models/` + `views/` → `mvc`

### 3. SPR Discovery
**Goal**: Find the System Personality Record (SPR) for the project.
**Mechanism**:
- Look for `.agents/{project_name}.md`.
- Look for `.agents/README.md`.
- Look for `README.md`.

### 4. Domain Context Extraction
**Goal**: Identify the Bounded Contexts of the application.
**Mechanism**:
- If DDD: Scan `domain/` or `src/*/domain` subdirectories.
- If MVC: Scan `models/` or `modules/`.

### 5. Configuration Generation
**Goal**: Create the `.sia.detected.yaml` file.
**Mechanism**:
- Compile all discovered data into the YAML schema defined in `STANDARDS.md`.
- Save to the project root.

---

## EXECUTION
The protocol is executed by the `sia/installer/auto_discovery.py` script, which is invoked by `sia/installer/install.sh`.

```bash
# Manual execution
python3 sia/installer/auto_discovery.py
```
