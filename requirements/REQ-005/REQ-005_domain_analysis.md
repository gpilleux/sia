# REQ-005 Domain Analysis: SIA 2.0 Autonomous Application

**Version**: 1.1 (Updated with repo_indexer integration)  
**Date**: 2025-11-25  
**Author**: Super Agent (Inception Mode)  
**Status**: DRAFT

---

## EXECUTIVE SUMMARY

**Critical Discovery**: The `repo_indexer` project already implements **Phase 2 (Knowledge Graph)** infrastructure with production-grade DDD architecture. This discovery reduces REQ-005 estimated effort from **120-160h → 80-100h** (33% reduction).

**Integration Strategy**: Create MCP server wrapper around `repo_indexer` using `fastmcp`, integrate as git submodule, expose semantic search + AST analysis as tools for SIA Super Agent.

---

## 1. ARCHITECTURAL DECISIONS

### 1.1 Knowledge Graph Infrastructure (REUSE DECISION)

**Decision**: Adopt `repo_indexer` as SIA's knowledge graph foundation instead of building from scratch.

**Evidence (from repo_indexer analysis)**:
- ✅ **Domain Layer**: Immutable entities (`CodeChunk`, `CodeChange`, `FileMetadata`) with Repository interfaces (`IVectorStore`, `ICodeChangeRepository`, `IFileMetadataRepository`)
- ✅ **Application Layer**: Use cases (`IndexRepositoryUseCase`, `QueryCodebaseUseCase`, `DeepDiveAnalysisUseCase`)
- ✅ **Infrastructure**: PostgreSQL 15 + pgvector (768-dim embeddings) + TimescaleDB (hypertables for temporal tracking)
- ✅ **AST Analysis**: `PythonASTAnalyzer` extracts classes/functions/imports with metadata (lines, decorators, docstrings)
- ✅ **Embeddings**: Google Gemini `text-embedding-004` (768-dim) via `EmbeddingService`
- ✅ **Testing**: 9 unit tests passing (domain + infrastructure layers)

**Missing Component**: MCP server implementation (marked as "Phase 3 🚧 In Progress" but no code exists).

**Justification**:
1. **DDD Compliance**: repo_indexer follows exact DDD patterns SIA requires (Domain → Application → Infrastructure → API)
2. **Production Ready**: Tested infrastructure with 927 chunks indexed, <2s search latency, incremental updates via AST hash comparison
3. **Technology Alignment**: Uses Google Gemini (same LLM family), PostgreSQL (robust), pgvector (industry standard for embeddings)
4. **Effort Reduction**: Building equivalent infrastructure from scratch = 30-40h, creating MCP wrapper = 5-8h

### 1.2 MCP Server Wrapper Design

**Pattern**: FastMCP server that delegates to repo_indexer Application layer use cases.

**Architecture**:
```
Claude Desktop / VS Code Copilot
    ↓ (MCP protocol - stdio transport)
FastMCP Server (repo_indexer_mcp.py)
    ↓ (Method calls)
Application Layer Use Cases
    ↓ (Repository interfaces)
Infrastructure (PostgreSQL + pgvector)
```

**Tool Definitions** (based on deepwiki research on jlowin/fastmcp):

```python
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from application.index_repository import IndexRepositoryUseCase
from application.query_codebase import QueryCodebaseUseCase

mcp = FastMCP("Repository Indexer")

@mcp.tool
async def index_repository(
    repo_path: str,
    repo_name: str,
    force_reindex: bool = False,
    ctx: Context = None
) -> str:
    """Index a repository using AST analysis and semantic embeddings.
    
    Args:
        repo_path: Absolute path to repository root
        repo_name: Unique identifier for the repository
        force_reindex: If True, re-index all files (ignore AST hash cache)
        ctx: MCP context for progress reporting
    
    Returns:
        JSON summary: {files_indexed, chunks_created, chunks_skipped, elapsed_time}
    """
    # Delegate to IndexRepositoryUseCase
    # Report progress via ctx.report_progress(current, total, message)
    pass

@mcp.tool
async def search_code(
    repo_name: str,
    query: str,
    top_k: int = 10,
    min_similarity: float = 0.5
) -> str:
    """Semantic search across codebase using natural language.
    
    Args:
        repo_name: Repository to search
        query: Natural language query (e.g., "vector store implementation")
        top_k: Maximum results to return
        min_similarity: Minimum cosine similarity threshold (0-1)
    
    Returns:
        JSON array of results: [{file_path, chunk_type, content, similarity, lines}]
    """
    # Delegate to QueryCodebaseUseCase
    pass

@mcp.tool
async def get_file_metadata(
    repo_name: str,
    file_path: str
) -> str:
    """Retrieve AST metadata for a specific file.
    
    Args:
        repo_name: Repository identifier
        file_path: Relative path to file
    
    Returns:
        JSON metadata: {ast_hash, last_indexed, chunk_count, imports, classes, functions}
    """
    # Query IFileMetadataRepository
    pass
```

**Error Handling** (per fastmcp patterns):
- Raise `ToolError` for user-actionable errors (missing repo, invalid path)
- Let infrastructure exceptions bubble up (database connection errors logged)

**Transport**: STDIO (default for `mcp.run()`), suitable for local Claude Desktop integration.

### 1.3 Embedding Model Validation

**Current Implementation**: Google Gemini `text-embedding-004` (768 dimensions)

**Research Status**: PENDING - Need deepwiki query to langchain-ai/langchain for comparison with:
- OpenAI `text-embedding-3-small` (1536-dim, $0.02/1M tokens)
- OpenAI `text-embedding-3-large` (3072-dim, $0.13/1M tokens)
- Local models (sentence-transformers/all-MiniLM-L6-v2, 384-dim, free but lower quality)

**Preliminary Assessment**:
- ✅ **Gemini Advantage**: Free tier (generous limits), integrated with Gemini LLM for consistency
- ✅ **Dimensionality**: 768-dim is balanced (not over-parameterized like 3072-dim)
- ⚠️ **Unknowns**: Performance vs OpenAI on code embeddings, rate limits, cold start latency

**Decision Deferred**: Validate in REQ-005 Phase 2A after deepwiki research. Migration path exists (repo_indexer has `EmbeddingService` abstraction).

### 1.4 Integration Strategy (Git Submodule)

**Pattern**: Add `repo_indexer` as git submodule in `sia/` (similar to existing submodule distribution pattern).

**Directory Structure**:
```
sia/
├── core/
├── agents/
├── skills/
├── requirements/
├── installer/
├── mcp_servers/                    # NEW
│   └── repo_indexer_mcp.py        # FastMCP wrapper
└── external/                       # NEW
    └── repo_indexer/               # Git submodule
        ├── domain/
        ├── application/
        ├── infrastructure/
        └── tests/
```

**Auto-Configuration** (via `installer/smart_init.py`):
1. Detect if `repo_indexer` submodule is initialized
2. Install dependencies: `uv pip install -e external/repo_indexer`
3. Start PostgreSQL via Docker Compose (if not running)
4. Generate MCP server config for Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`)
5. Index target repository on first run

**Claude Desktop Config** (auto-generated):
```json
{
  "mcpServers": {
    "repo-indexer": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/gpilleux/apps/meineapps/sia",
        "python",
        "mcp_servers/repo_indexer_mcp.py"
      ],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}",
        "DATABASE_URL": "postgresql+asyncpg://indexer:indexer123@localhost:5436/repo_indexer"
      }
    }
  }
}
```

---

## 2. DOMAIN MODEL REFINEMENT

### 2.1 Existing Domain Entities (from repo_indexer)

**Core Entities** (immutable dataclasses):

```python
@dataclass(frozen=True)
class CodeChunk:
    """Represents a semantic code unit (function, class, module).
    
    Invariants:
    - chunk_type in {'function', 'class', 'module', 'docstring'}
    - content must be non-empty
    - metadata contains {line_start, line_end, imports, dependencies}
    """
    id: UUID
    repo_name: str
    file_path: str
    chunk_type: str
    chunk_name: Optional[str]  # Function/class name
    content: str  # Full source code (for embedding)
    metadata: Optional[Dict[str, Any]]
    indexed_at: datetime

@dataclass(frozen=True)
class CodeChange:
    """Git commit event for temporal analysis (TimescaleDB hypertable).
    
    Invariants:
    - change_type in {'added', 'modified', 'deleted'}
    - time must be timezone-aware (UTC)
    - lines_added/deleted >= 0
    """
    id: UUID
    time: datetime
    repo_name: str
    commit_hash: str
    file_path: str
    change_type: str
    lines_added: int
    lines_deleted: int
    diff_content: Optional[str]

@dataclass(frozen=True)
class FileMetadata:
    """File-level metadata for incremental indexing.
    
    Invariants:
    - ast_hash is SHA-256 of normalized AST structure
    - last_indexed <= datetime.now(UTC)
    """
    id: UUID
    repo_name: str
    file_path: str
    ast_hash: str  # For change detection
    last_indexed: datetime
```

**Repository Interfaces** (Dependency Inversion):
- `IVectorStore`: Semantic search operations (add_chunks, search, delete_file_chunks)
- `ICodeChangeRepository`: Temporal tracking (save, query_range, get_by_file)
- `IFileMetadataRepository`: Incremental indexing (get_by_path, save, update_hash)

### 2.2 SIA-Specific Domain Extensions (NEW)

**For Skills API (Phase 3)**:

```python
@dataclass(frozen=True)
class SkillExecution:
    """Represents a skill execution event (DDD aggregate root).
    
    Invariants:
    - status in {'pending', 'running', 'completed', 'failed'}
    - if status == 'failed', error_message must be non-empty
    - execution_time_ms >= 0
    """
    id: UUID
    skill_name: str  # 'check_complexity', 'audit_ddd', etc.
    repo_name: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    execution_time_ms: int
    result: Optional[Dict[str, Any]]  # Skill-specific output
    error_message: Optional[str]

@dataclass(frozen=True)
class DomainViolation:
    """DDD/SOLID violation detected by audit_ddd skill.
    
    Invariants:
    - severity in {'error', 'warning', 'info'}
    - line_number > 0
    - rule_id matches pattern '^[A-Z]{3}-\\d{3}$' (e.g., 'DIP-001')
    """
    id: UUID
    repo_name: str
    file_path: str
    line_number: int
    rule_id: str  # DIP-001, SRP-002, etc.
    severity: str
    message: str
    detected_at: datetime
```

**New Repository Interfaces**:
- `ISkillExecutionRepository`: Track skill runs, query history, analyze trends
- `IDomainViolationRepository`: Store audit findings, generate compliance reports

### 2.3 Value Objects

```python
@dataclass(frozen=True)
class Embedding:
    """768-dimensional vector representation of code chunk.
    
    Invariants:
    - dimensions == 768 (Gemini text-embedding-004)
    - All values in range [-1, 1] (cosine normalized)
    """
    vector: List[float]
    model: str = "text-embedding-004"
    
    def cosine_similarity(self, other: 'Embedding') -> float:
        """Compute cosine similarity with another embedding."""
        pass

@dataclass(frozen=True)
class ComplexityMetrics:
    """Code complexity measurements (from check_complexity skill).
    
    Invariants:
    - cyclomatic_complexity >= 1 (minimum for any function)
    - rank in {'A', 'B', 'C', 'D', 'E', 'F'}
    - maintainability_index in [0, 100]
    """
    cyclomatic_complexity: int
    rank: str  # Radon rank
    maintainability_index: float
    halstead_difficulty: Optional[float]
```

---

## 3. TECHNOLOGY STACK VALIDATION

### 3.1 Database Layer

**Decision**: PostgreSQL 15 + pgvector + TimescaleDB (APPROVED - from repo_indexer)

**Rationale**:
- ✅ **pgvector**: Industry standard for embeddings (used by LangChain, Supabase, etc.)
- ✅ **ivfflat index**: Fast KNN search with configurable recall/speed tradeoff (lists=100 default)
- ✅ **TimescaleDB**: Production-grade time-series extension (used by Grafana, AWS Timestream competitor)
- ✅ **Continuous Aggregates**: Automatic rollups for daily/weekly code change metrics
- ✅ **Compression Policies**: Columnstore compression after 7 days (storage optimization)

**Schema Highlights** (from repo_indexer):
```sql
-- Semantic search (pgvector)
CREATE TABLE code_chunks (
    embedding vector(768),  -- Gemini text-embedding-004
    -- ... other columns
);
CREATE INDEX ON code_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Temporal analysis (TimescaleDB hypertable)
SELECT create_hypertable('code_changes', 'time', chunk_time_interval => INTERVAL '1 day');

-- Continuous aggregate (auto-updating materialized view)
CREATE MATERIALIZED VIEW daily_changes AS
SELECT
    time_bucket('1 day', time) AS day,
    repo_name,
    COUNT(*) as file_count,
    SUM(lines_added) as total_additions
FROM code_changes
GROUP BY day, repo_name;
```

**Performance** (from repo_indexer testing):
- Indexing: 0.25-0.3 files/sec (Gemini API rate limited)
- Search: <2s latency (embedding generation + KNN query)
- Memory: <500MB for 927 chunks
- Incremental: AST hash comparison skips unchanged files (0/24 re-indexed in test)

### 3.2 AST Analysis

**Decision**: Use `repo_indexer.infrastructure.services.ast_analyzer.PythonASTAnalyzer` (APPROVED)

**Capabilities** (verified from source):
- Extract classes with methods, docstrings, decorators
- Extract standalone functions with signatures
- Extract module-level docstrings and imports
- Line number tracking (for code navigation)
- Metadata: `{line_start, line_end, imports: [...], decorators: [...]}`

**Pattern** (from deepwiki research on python/cpython):
```python
import ast

# Safe parsing (handles syntax errors)
try:
    tree = ast.parse(source_code)
except SyntaxError as e:
    logger.error(f"Syntax error at line {e.lineno}: {e.msg}")
    return []

# Visitor pattern for traversal
class FunctionVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        # Extract function metadata
        chunk = CodeChunk(
            chunk_type='function',
            chunk_name=node.name,
            content=ast.get_source_segment(source_code, node),
            metadata={
                'line_start': node.lineno,
                'line_end': node.end_lineno,
                'decorators': [ast.unparse(d) for d in node.decorator_list]
            }
        )
        self.generic_visit(node)  # Continue traversal
```

### 3.3 Embedding Service

**Current**: Google Gemini `text-embedding-004` (768-dim)

**API Pattern** (from repo_indexer):
```python
import google.generativeai as genai

genai.configure(api_key=settings.gemini_api_key)

embedding = await genai.embed_content(
    model="models/text-embedding-004",
    content=code_text,  # Full function/class source
    task_type="retrieval_document"  # vs "retrieval_query" for search
)
```

**Batch Optimization** (needed for large repos):
- Gemini supports batch embedding (up to 100 requests/batch)
- Rate limits: 1500 requests/minute (free tier)
- Strategy: Chunk indexing in batches of 50, parallel execution with asyncio.gather()

**Pending Research**: Compare with OpenAI embeddings (deepwiki on langchain-ai/langchain).

### 3.4 MCP Server Framework

**Decision**: `fastmcp` (APPROVED - from deepwiki research)

**Key Patterns**:
1. **Tool Definition**: `@mcp.tool` decorator auto-generates schema from type hints
2. **Async Support**: Native async/await with `Context` injection for progress reporting
3. **Error Handling**: `ToolError` for user-actionable errors, other exceptions logged
4. **Transport**: STDIO (default) for Claude Desktop, HTTP optional for web integration
5. **Type Safety**: Enforces type hints, generates JSON schema for MCP protocol

**Example** (from deepwiki):
```python
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError

mcp = FastMCP("My Server")

@mcp.tool
async def complex_task(param: str, ctx: Context) -> str:
    """Long-running task with progress reporting."""
    await ctx.report_progress(0.5, 1.0, "Halfway done")
    # ... work
    if error_condition:
        raise ToolError("User-friendly error message")
    return result

if __name__ == "__main__":
    mcp.run()  # STDIO transport by default
```

### 3.5 Testing Framework

**Decision**: pytest + pytest-asyncio + pytest-order (APPROVED - from repo_indexer)

**Current Coverage** (repo_indexer):
- 9 unit tests passing
- Fixtures: `async_session`, `vector_store`, `embedding_service`
- Scope: Domain entities, AST analyzer, vector store operations

**Gaps to Address** (REQ-005 Phase 4):
- Integration tests (database-dependent workflows)
- E2E tests (MCP tool invocation end-to-end)
- Parametrized tests for edge cases (empty files, syntax errors, large repos)

**Pattern** (from deepwiki on pytest-dev/pytest):
```python
import pytest

@pytest.mark.asyncio
async def test_semantic_search(vector_store, async_session):
    """Test semantic search returns relevant results."""
    # Arrange
    chunks = [create_test_chunk(...)]
    await vector_store.add_chunks(chunks)
    
    # Act
    results = await vector_store.search(
        query="vector store implementation",
        repo_name="test_repo",
        top_k=5
    )
    
    # Assert
    assert len(results) > 0
    assert results[0][1] > 0.7  # High similarity score
```

---

## 4. INVARIANTS & CONSTRAINTS

### 4.1 Knowledge Graph Invariants

1. **Embedding Consistency**: All chunks for a repository use same embedding model version
2. **AST Hash Uniqueness**: `file_metadata.ast_hash` deterministic for identical AST structure
3. **Chunk Completeness**: Every indexed file has at least 1 chunk (module-level)
4. **Temporal Ordering**: `code_changes.time` must be timezone-aware UTC
5. **Similarity Range**: pgvector cosine distance in [0, 2], similarity score in [0, 1]

### 4.2 MCP Tool Invariants

1. **Idempotency**: `index_repository` with same inputs produces same chunks (AST hash stable)
2. **Error Transparency**: All ToolError messages are actionable by user
3. **Progress Reporting**: Long operations (>5s) report progress via Context
4. **Result Serialization**: All tool returns are JSON-serializable strings

### 4.3 Performance Constraints

1. **Search Latency**: P95 < 2s for semantic search (top_k=10)
2. **Indexing Throughput**: >= 0.2 files/sec (accounting for Gemini rate limits)
3. **Memory Usage**: < 1GB for repos with <10K chunks
4. **Incremental Efficiency**: Skip >= 90% of unchanged files (AST hash comparison)

---

## 5. MIGRATION FROM SCRIPTS TO APPLICATION

### 5.1 Current SIA Skills → Future Skills API

**Legacy Pattern** (bash scripts):
```bash
#!/bin/bash
# skills/check_complexity.sh
radon cc repo_indexer -a -nb > analysis/complexity.txt
```

**Target Pattern** (DDD Application Layer):
```python
# application/check_complexity_use_case.py
class CheckComplexityUseCase:
    def __init__(
        self,
        code_chunk_repo: IVectorStore,
        complexity_repo: IComplexityMetricsRepository
    ):
        self._code_chunk_repo = code_chunk_repo
        self._complexity_repo = complexity_repo
    
    async def execute(self, repo_name: str) -> ComplexityReport:
        """Analyze cyclomatic complexity for all chunks in repo."""
        # Query all chunks
        chunks = await self._code_chunk_repo.get_by_repo(repo_name)
        
        # Run Radon analysis
        metrics = []
        for chunk in chunks:
            if chunk.chunk_type == 'function':
                cc = self._analyze_complexity(chunk.content)
                metrics.append(ComplexityMetrics(...))
        
        # Persist results
        await self._complexity_repo.save_batch(metrics)
        
        return ComplexityReport(metrics)
```

**MCP Tool** (API Layer):
```python
@mcp.tool
async def check_complexity(repo_name: str) -> str:
    """Analyze cyclomatic complexity for all functions in repository."""
    use_case = CheckComplexityUseCase(vector_store, complexity_repo)
    report = await use_case.execute(repo_name)
    return report.to_json()
```

### 5.2 REQ-004 Skills Integration

**REQ-004 Skills** (from audit):
1. `check_complexity.sh` → `CheckComplexityUseCase`
2. `visualize_architecture.sh` → `VisualizeArchitectureUseCase` (pydeps wrapper)
3. `check_coverage.sh` → `CheckCoverageUseCase` (pytest-cov wrapper)
4. `audit_ddd.py` → `AuditDDDUseCase` (enhanced with AST analysis from repo_indexer)
5. `metrics.py` → Deprecated (logic absorbed into other use cases)

**Strategy**: REQ-004 implementation becomes part of REQ-005 Phase 3 (Skills API). Bash scripts remain as fallback for non-Python projects.

---

## 6. RISK MITIGATION

### 6.1 Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Gemini API rate limits block indexing | HIGH | Implement exponential backoff, batch requests (50/batch), show progress in MCP tool |
| pgvector index build time on large repos | MEDIUM | Build index incrementally, use parallel indexing (asyncio.gather), show ETA |
| MCP server crashes break Claude integration | HIGH | Wrap all tools in try/except, log to file, return ToolError with recovery steps |
| AST parsing fails on syntax errors | LOW | Safe parsing (try/except SyntaxError), skip file with warning, continue indexing |
| Database migrations break existing data | MEDIUM | Version schemas, add migration scripts, backup before upgrades |

### 6.2 Integration Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| repo_indexer updates break SIA compatibility | HIGH | Pin git submodule to specific commit, test upgrades in staging branch |
| Claude Desktop config changes break MCP | MEDIUM | Auto-detect config location (macOS/Linux/Windows), validate JSON before write |
| Multiple SIA installations conflict on DB | LOW | Use repo-name-based database namespacing, document multi-project setup |

---

## 7. SUCCESS METRICS

### 7.1 Phase 2 Success Criteria (Knowledge Graph + MCP)

- [ ] MCP server exposes 3 tools (index_repository, search_code, get_file_metadata)
- [ ] Indexing SIA framework completes in <5 minutes (31 Python files)
- [ ] Semantic search query "DDD repository pattern" returns relevant results (similarity >0.7)
- [ ] MCP server runs stable for 1 hour without crashes
- [ ] Auto-configuration adds Claude Desktop config without manual editing

### 7.2 Dogfooding Validation

**Test Scenario**: Use SIA to develop REQ-005 Phase 3 (Skills API)

- [ ] Agent queries: "Show me all repository interfaces in SIA"
- [ ] Agent queries: "Find functions with cyclomatic complexity >10"
- [ ] Agent queries: "What DDD patterns are used in repo_indexer?"
- [ ] Agent generates new use case code using retrieved examples
- [ ] Agent validates generated code against DDD invariants (using audit_ddd)

---

## 8. NEXT STEPS

1. **Complete deepwiki research**: Query langchain-ai/langchain for embedding model comparison ⏳
2. **Create REQ-005_quant_breakdown.md**: Decompose into 50-70 atomic tasks (reduced from 80) ⏳
3. **Prototype MCP wrapper**: Implement `repo_indexer_mcp.py` with 3 tools (2-3h) 🎯
4. **Test integration**: Index SIA, run semantic search via Claude Desktop 🧪
5. **Update REQ-005.md**: Finalize Phase 2 estimates with integration findings 📝

---

## APPENDIX A: Deepwiki Research Summary

### A.1 FastMCP Patterns (jlowin/fastmcp)

**Key Findings**:
- Tool schema auto-generated from type hints (no manual JSON)
- Context injection for progress reporting (`ctx.report_progress(current, total, message)`)
- ToolError for user-actionable errors, other exceptions logged/masked
- STDIO transport default (suitable for Claude Desktop)
- HTTP transport available (`mcp.run(transport="http", host="0.0.0.0", port=8000)`)

**Code Example**:
```python
@mcp.tool
async def long_task(duration: float, ctx: Context) -> str:
    """Simulate long-running task with progress."""
    for i in range(int(duration)):
        await ctx.report_progress(i+1, duration, f"Step {i+1}/{duration}")
        await asyncio.sleep(1)
    return f"Completed {duration} steps"
```

### A.2 repo_indexer Architecture Analysis

**Verified Capabilities**:
- ✅ Domain entities: `CodeChunk`, `CodeChange`, `FileMetadata` (frozen dataclasses)
- ✅ Repository interfaces: `IVectorStore`, `ICodeChangeRepository`, `IFileMetadataRepository`
- ✅ Use cases: `IndexRepositoryUseCase`, `QueryCodebaseUseCase`, `DeepDiveAnalysisUseCase`
- ✅ Infrastructure: `PostgresVectorStore` (pgvector + Gemini), `PythonASTAnalyzer`, `EmbeddingService`
- ✅ Database schema: Hypertables, continuous aggregates, compression policies
- ✅ Testing: 9 unit tests (pytest + pytest-asyncio)

**Gaps**:
- ❌ MCP server (Phase 3 marked "In Progress" but no implementation)
- ❌ Git change detection (TimescaleDB schema exists, no indexing logic)
- ⚠️ Integration tests (only unit tests for isolated components)

### A.3 Pending Research

**Questions for langchain-ai/langchain**:
1. How does LangChain integrate pgvector with different embedding models?
2. What are best practices for batch embedding large codebases?
3. Comparison: Gemini text-embedding-004 vs OpenAI text-embedding-3-small for code search
4. How to handle embedding model migrations (re-indexing strategy)?

**Questions for openai/openai-python**:
1. Embedding API best practices (batching, rate limits, error handling)
2. Cost optimization strategies for large-scale indexing
3. Model selection: text-embedding-3-small vs text-embedding-3-large for code

**Questions for huggingface/transformers**:
1. Local embedding models for code (CodeBERT, GraphCodeBERT alternatives)
2. sentence-transformers optimization (quantization, ONNX export)
3. Trade-offs: local inference (latency, quality) vs API (cost, rate limits)

---

**Document Status**: DRAFT (awaiting deepwiki research completion)  
**Next Review**: After QUANT breakdown creation  
**Approver**: Super Agent (Inception Mode)
