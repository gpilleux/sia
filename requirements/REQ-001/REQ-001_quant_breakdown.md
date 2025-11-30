# REQ-001: QUANT TASK DECOMPOSITION - Multi-Tenant + Demo + Auth

**Requirement**: Multi-Tenant SaaS Architecture + Demo Sandbox + Authentication  
**Decomposition Date**: 2025-11-23 (REVISED - Final)  
**Total Effort**: 38h over 2 phases

---

## OBJECTIVE

Implement **robust multi-tenant SaaS architecture** enabling:
1. Multiple clients with zero data collision (DB-enforced isolation)
2. Demo sandbox in parallel (is_demo=TRUE company)
3. Authentication for real data access
4. Rapid client onboarding (<2 min per company)

---

## CENTRAL INVARIANTS

```
∀ entity ∈ DomainEntities:
    entity.company_id → Companies.id (FK enforced)

∀ query(user):
    authenticated → filter(company_id = user.company_id)
    unauthenticated → filter(company_id = DEMO_COMPANY_ID)

∀ company_A ≠ company_B:
    data(A) ∩ data(B) = ∅
```

---

## EXECUTION PLAN

### **PHASE 1: Multi-Tenant Foundation** (25h, 4-5 days)

1. **Q-101** (6h) - DB migration: Add company_id to 10+ tables
2. **Q-102** (2h) - Backfill data + FK constraints
3. **Q-103** (2h) - Domain: Sales entities (Customer, Product, Order)
4. **Q-104** (1.5h) - Domain: CRM entities (Lead, Opportunity) [PARALLEL]
5. **Q-105** (1.5h) - Domain: Accounting entities (Invoice, Payment) [PARALLEL]
6. **Q-106** (4h) - Repositories: Company filtering (all modules)
7. **Q-107** (3h) - Use cases: Accept company_id parameter
8. **Q-108** (5h) - Tests: Update 364 tests

### **PHASE 2: Auth + Demo** (13h, 2 days)

9. **Q-201** (1.5h) - Auth infrastructure (JWT, passwords)
10. **Q-202** (1h) - Company context middleware
11. **Q-203** (1h) - Auth endpoints (login/logout) [PARALLEL with Q-204]
12. **Q-204** (2h) - Demo seed data [PARALLEL with Q-203]
13. **Q-205** (3h) - API routes: Inject company_id (71 endpoints)
14. **Q-206** (1.5h) - Frontend: AuthContext
15. **Q-207** (1h) - Frontend: Demo banner
16. **Q-208** (2h) - E2E: Multi-tenant flows

**Critical Path**: Q-101→Q-102→Q-103→Q-106→Q-107→Q-108→Q-201→Q-202→Q-205→Q-208 (34h with parallelism)

---

## PHASE 1 QUANTASKS (Detailed)

### Q-101: Database Migration - Add company_id

**Effort**: 6h | **Risk**: HIGH  
**Layer**: Infrastructure (Schema)

**What**: Add `company_id UUID` to customers, products, sale_orders, addresses, leads, opportunities, invoices, payments, payment_schedules (10 tables)

**Acceptance**:
- [ ] Column exists with NULL allowed (for backfill)
- [ ] Indexes created: `idx_{table}_company_id`
- [ ] Migration rollback tested

**Files**:
- `backend/alembic/versions/add_company_id_to_tables.py` (CREATE)
- `init.sql` (UPDATE for fresh installs)

**SQL**:
```sql
ALTER TABLE customers ADD COLUMN company_id UUID;
CREATE INDEX idx_customers_company_id ON customers(company_id);
-- Repeat for 9 other tables
```

---

### Q-102: Backfill Data + FK Constraints

**Effort**: 2h | **Risk**: MEDIUM  
**Layer**: Infrastructure (Data)

**What**: Set company_id = '81db4b3b...' (Demo Company Chile) for existing records, add FK constraints, make NOT NULL

**Acceptance**:
- [ ] Zero NULL company_id records
- [ ] FK constraints enforced
- [ ] Validation queries pass

**SQL**:
```sql
UPDATE customers SET company_id = '81db4b3b-ac5a-42f2-8ce5-8528eb4a91d1';
ALTER TABLE customers ALTER COLUMN company_id SET NOT NULL;
ALTER TABLE customers ADD CONSTRAINT fk_customers_company 
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE RESTRICT;
```

---

### Q-103 to Q-105: Domain Entities (Sales, CRM, Accounting)

**Effort**: 5h (2h + 1.5h + 1.5h) | **Risk**: MEDIUM  
**Layer**: Domain

**What**: Add `company_id: UUID` field to Customer, Product, Order, Lead, Opportunity, Invoice, Payment entities

**Pattern** (Sales module example):
```python
class Customer(AggregateRoot):
    def __init__(
        self,
        name: str,
        company_id: UUID,  # ✅ NEW
        email: Optional[Email] = None,
        ...
    ):
        self._company_id = company_id
    
    @property
    def company_id(self) -> UUID:
        return self._company_id
```

**Acceptance**:
- [ ] All entities have company_id property
- [ ] Immutability preserved (frozen)
- [ ] Unit tests pass

---

### Q-106: Repositories - Company Filtering

**Effort**: 4h | **Risk**: HIGH  
**Layer**: Infrastructure (Repositories)

**What**: Implement `find_by_company(company_id)` and `find_by_id_and_company(id, company_id)` in all repositories

**Pattern**:
```python
# Interface
class ICustomerRepository(ABC):
    @abstractmethod
    async def find_by_company(self, company_id: UUID) -> List[Customer]:
        pass

# Implementation
class PostgresCustomerRepository:
    async def find_by_company(self, company_id: UUID) -> List[Customer]:
        query = select(CustomerModel).where(
            CustomerModel.company_id == company_id
        )
        result = await self.session.execute(query)
        return [self._to_entity(m) for m in result.scalars().all()]
```

**Acceptance**:
- [ ] All repos have find_by_company()
- [ ] Cross-tenant access returns empty list
- [ ] Integration tests validate isolation

---

### Q-107: Use Cases - company_id Parameter

**Effort**: 3h | **Risk**: MEDIUM  
**Layer**: Application

**What**: Update use cases to accept company_id, pass to repositories

**Pattern**:
```python
# BEFORE
async def execute(self, dto: CreateCustomerDTO) -> Customer:
    customer = Customer(name=dto.name, ...)

# AFTER
async def execute(self, dto: CreateCustomerDTO, company_id: UUID) -> Customer:
    customer = Customer(name=dto.name, company_id=company_id, ...)
```

**Acceptance**:
- [ ] All CRUD use cases updated
- [ ] Entities created have correct company_id
- [ ] Unit tests mock company_id

---

### Q-108: Tests - Update 364 Tests

**Effort**: 5h | **Risk**: HIGH  
**Layer**: All layers

**What**: Update all tests to use company_id fixtures, add isolation tests

**Pattern**:
```python
@pytest.fixture
def test_company_a():
    return UUID("aaaa-aaaa-aaaa-aaaa")

def test_create_customer(test_company_a):
    customer = Customer(name="Acme", company_id=test_company_a)
    assert customer.company_id == test_company_a

async def test_multi_tenant_isolation(company_a, company_b, repo):
    """Company A cannot see Company B data"""
    customer_a = await repo.save(Customer(..., company_id=company_a))
    result = await repo.find_by_id_and_company(customer_a.id, company_b)
    assert result is None  # ✅ Blocked
```

**Acceptance**:
- [ ] 364/364 tests pass
- [ ] New isolation tests added
- [ ] Coverage >= 85%

---

## PHASE 2 QUANTASKS (Summary)

**NOTE**: Phase 2 is simpler because Phase 1 handles multi-tenancy. These are standard auth tasks.

### Q-201: Auth Infrastructure (JWT, Passwords)
- python-jose for JWT
- passlib for bcrypt
- Config from environment

### Q-202: Company Context Middleware
```python
async def get_company_context(request: Request) -> UUID:
    token = extract_jwt(request)
    return token.company_id if token else DEMO_COMPANY_ID
```

### Q-203: Auth Endpoints
- POST /auth/login → JWT
- POST /auth/logout (client-side)

### Q-204: Demo Seed Data
- Insert DEMO_COMPANY with is_demo=TRUE
- Seed 10 customers, 20 products, 15 orders

### Q-205: API Routes - Company Injection
```python
@router.get("/customers")
async def list_customers(
    company_id: UUID = Depends(get_company_context)
):
    return await repo.find_by_company(company_id)
```

### Q-206-Q-207: Frontend (AuthContext + Demo Banner)
- React context for JWT storage
- Demo banner when !authenticated

### Q-208: E2E Tests
- Playwright: Demo mode → Login → See real data
- Validate isolation (Company A vs Company B)

---

## SUCCESS METRICS

### Phase 1 Done:
- ✅ All tables have company_id FK
- ✅ 364 tests green
- ✅ Cross-tenant access = 404

### Phase 2 Done:
- ✅ Demo mode works (no auth)
- ✅ Admin login sees real data
- ✅ New client setup <2 min

### Production Ready:
- ✅ DB backup + rollback plan
- ✅ E2E tests all flows
- ✅ Performance profiling (queries <100ms)

---

## RISK MITIGATION

| Risk | Mitigation |
|------|------------|
| Migration fails | Dry-run on DB clone, rollback script ready |
| Tests break | Incremental updates, module-by-module |
| Performance issues | Indexes on company_id, query profiling |
| Data leak | E2E tests validate isolation, FK constraints |

---

## ARCHITECTURAL DECISIONS

**ADR-1**: Multi-tenant via company_id (NOT Row-Level Security)  
**Why**: KISS, debuggable, proven (Purchase module)

**ADR-2**: FK ON DELETE RESTRICT (NOT CASCADE)  
**Why**: Safety (prevent accidental data loss)

**ADR-3**: Demo as regular company (NOT separate schema)  
**Why**: Same code path, easy reset

---

## NEXT: IMPLEMENTATION

Ready to create branch and start implementation.

**Command**:
```bash
git checkout -b feature/multi-tenant-foundation
git push -u origin feature/multi-tenant-foundation
```

Then start with Q-101 (DB migration).
