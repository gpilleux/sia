# SIA Test Suite

Automated tests for SIA framework installer and core components.

## Test Strategy: Isolated Temporary Environments

**Problem**: Testing installer without contaminating local `.sia/` directory.

**Solution**: Use `tempfile.TemporaryDirectory()` + pytest fixtures to create disposable test projects.

## Running Tests

### Quick Test (Local)

```bash
# From SIA repository root
uv run pytest tests/test_installer.py -v
```

### Full Test Suite

```bash
# Run all tests with coverage
uv run pytest tests/ -v --cov=installer --cov-report=html

# Run specific test class
uv run pytest tests/test_installer.py::TestSIAInstaller -v

# Run specific test
uv run pytest tests/test_installer.py::TestSIAInstaller::test_install_py_creates_structure -v
```

### Docker Tests (Cross-Platform Validation)

```bash
# Run Docker-based tests (requires Docker installed)
uv run pytest tests/test_installer.py -v -m docker
```

**Note**: Docker tests are skipped by default. Enable with `-m docker` flag.

## Test Coverage

### `test_installer.py`

**TestSIAInstaller**:
- ✅ `test_install_py_creates_structure` - Verifies directory creation
- ✅ `test_install_py_creates_readme_files` - Validates README generation
- ✅ `test_install_py_creates_config_files` - Checks YAML/JSON/MD configs
- ✅ `test_install_py_installs_slash_commands` - Verifies 11 prompt files
- ✅ `test_install_py_creates_gitignore` - Validates .gitignore template
- ✅ `test_install_py_respects_existing_files` - Non-destructive installer
- ✅ `test_install_py_auto_discovery_runs` - Validates smart_init integration
- ✅ `test_install_sh_parity` - Ensures install.sh matches install.py
- ✅ `test_installer_idempotency` - Safe to run multiple times
- ✅ `test_python_version_check` - Validates Python 3.10+ requirement

**TestSmartInit**:
- ✅ `test_smart_init_generates_yaml` - Validates auto-discovery YAML output

**TestDockerIntegration** (manual):
- 🐳 `test_install_in_ubuntu_container` - Ubuntu 22.04 validation
- 🐳 `test_install_in_alpine_container` - Alpine Linux validation

## How Tests Work

### Fixture: `temp_project`

```python
@pytest.fixture
def temp_project(self):
    """Create isolated temporary project with SIA framework"""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "test_project"
        # Copy SIA framework (excluding .git, .sia, __pycache__)
        # Yield to test
        # Automatic cleanup on exit
```

**Key Benefits**:
- ✅ No contamination of local SIA installation
- ✅ Clean state for each test
- ✅ Automatic cleanup (no manual deletion)
- ✅ Parallel test execution safe

### Example Test Flow

```python
def test_install_py_creates_structure(temp_project):
    # 1. Run installer in temp directory
    subprocess.run(["python3", "sia/installer/install.py"], cwd=temp_project)
    
    # 2. Verify structure created
    assert (temp_project / ".sia/agents").exists()
    
    # 3. Temp directory auto-deleted after test
```

## CI/CD Integration

### GitHub Actions Workflow (Future)

```yaml
name: Test SIA Installer
on: [push, pull_request]
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install uv pytest pytest-cov
      - run: uv run pytest tests/ -v --cov
```

## Adding New Tests

### Test Checklist

1. **Isolation**: Use `temp_project` fixture
2. **Cleanup**: No manual cleanup (fixture handles it)
3. **Assertions**: Clear error messages
4. **Documentation**: Docstring explaining test purpose

### Example New Test

```python
def test_install_creates_custom_file(self, temp_project):
    """Test that installer creates custom project file"""
    # Run installer
    subprocess.run(["python3", "sia/installer/install.py"], cwd=temp_project)
    
    # Verify file
    custom_file = temp_project / ".sia/custom.txt"
    assert custom_file.exists(), "Custom file not created"
    assert "expected content" in custom_file.read_text()
```

## Troubleshooting

### Test Fails: "Permission denied"

**Cause**: Script not executable in temp directory.

**Solution**: Tests use explicit interpreter (`python3 sia/installer/install.py` instead of `./install.py`).

### Test Fails: "Module not found"

**Cause**: Missing test dependencies.

**Solution**:
```bash
uv pip install pytest pytest-cov
```

### Test Hangs

**Cause**: Installer waiting for user input.

**Solution**: Ensure installer runs in non-interactive mode. Use `capture_output=True` in subprocess.

## Performance

- **Single test**: ~2-5 seconds (includes temp dir creation + installer run)
- **Full suite**: ~30-60 seconds (10+ tests)
- **Docker tests**: ~5-10 minutes (image build + container spawn)

## Future Enhancements

- [ ] Windows-specific tests (`.bat` installer)
- [ ] Docker integration tests (Ubuntu, Alpine, Debian)
- [ ] Performance benchmarks (installer speed)
- [ ] Snapshot testing (compare generated files with golden copies)
- [ ] Integration with MCP server tests
- [ ] Auto-discovery test suite (tech stack detection)

## References

- **pytest fixtures**: https://docs.pytest.org/en/stable/fixture.html
- **tempfile module**: https://docs.python.org/3/library/tempfile.html
- **subprocess testing**: https://docs.python.org/3/library/subprocess.html
